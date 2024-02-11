from datetime import datetime
from pathlib import Path

import feedparser

FEED_URL = "https://enchantedcode.co.uk/blog/feed.xml"
PUBLISHED_BEFORE = datetime(2024, 1, 1)

def make_filename(date, slug):
    return Path("content/posts", f"{date.year}-{date.month:02d}-{date.day:02d}-{slug}.md")


def extract_data(entry):
    return {
        "link": entry.link,
        "slug": entry.link.split("https://enchantedcode.co.uk/blog/")[1].split("/")[0],
        "title": entry.title,
        "published": datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %z"),
    }


def filter_new(entry):
    slug = entry["slug"]
    published = entry["published"]
    if published.replace(tzinfo=None) < PUBLISHED_BEFORE:
        return False
    return not make_filename(published, slug).is_file()


def write_entry(entry):
    content = f"""---
title: \"{entry["title"]}\"
date: {entry['published'].strftime("%Y-%m-%dT%H:%M:%SZ")}
description: "New blog post '{entry["title"]}' released."
tags:
    - blog
---

[![Post featured image](https://assets.enchantedcode.co.uk/blog/{entry["slug"]}/featured.png)](https://enchantedcode.co.uk/blog/{entry["slug"]}/)

Come and read '{entry["title"]}' at: [enchantedcode.co.uk](https://enchantedcode.co.uk/blog/{entry["slug"]}/) as it's now published!
"""
    with open(make_filename(entry["published"], entry["slug"]), "wt") as fo:
        fo.write(content)


def main():
    feed = feedparser.parse(FEED_URL)
    entries = filter(filter_new, map(extract_data, feed.entries))

    for entry in entries:
        print(f"ingesting {entry['title']}")
        write_entry(entry)

    print("done")

if __name__ == "__main__":
    main()
