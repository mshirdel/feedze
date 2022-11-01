import ssl

import feedparser

from scraper.domain.entry import Entry
from scraper.domain.feed import Feed


class FeedScraper:
    def __init__(self, url: str):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.url = url
        self.feed = Feed()
        self.entries = []

    def _convert_feed(self, parsed_feed):
        self.feed.title = parsed_feed.get("title")
        self.feed.link = parsed_feed.get("link")
        self.feed.published = parsed_feed.get("published")
        self.feed.published_parsed = parsed_feed.get("published_parsed")
        self.feed.updated = parsed_feed.get("updated")
        self.feed.updated_parsed = parsed_feed.get("updated_parsed")
        self.feed.image_url = parsed_feed.get("image", {}).get("href")
        self.feed.description = parsed_feed.get("description", "")
        self.feed.validate()

    def _convert_entries(self, parsed_entries):
        for entry in parsed_entries:
            e = Entry(
                title=entry.get("title"),
                link=entry.get("link"),
                author=entry.get("author"),
                published=entry.get("published)"),
                summary=entry.get("summary"),
                content=entry.get("content"),
                published_parsed=entry.get("published_parsed"),
            )
            self.entries.append(e)

    def scrap(self):
        parsed_feed = feedparser.parse(self.url)
        self._convert_feed(parsed_feed.feed)
        self._convert_entries(parsed_feed.entries)
