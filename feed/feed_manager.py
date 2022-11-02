from datetime import datetime
from time import mktime

import pytz

from scraper.domain.feed import Feed
from scraper.exceptions import FeedException
from scraper.feed_scrapper import FeedScraper
from feed.models import Feed as FeedModel, FeedItem


class FeedUpdater:
    def __init__(self, feed: FeedModel):
        self.feed_model = feed

    def update(self) -> bool:
        scraper = FeedScraper(url=self.feed_model.feed_url)
        feed, entries = scraper.scrap()
        if not self._check_for_update(feed):
            return False
        for entry in entries:
            FeedItem.objects.get_or_create(
                feed=self.feed_model,
                title=entry.title,
                description=entry.title,
                link=entry.link,
                author=entry.author,
                published_at=datetime.utcfromtimestamp(mktime(entry.published_parsed)),
            )
        return True

    def _check_for_update(self, feed: Feed):
        feed_updated_parsed = datetime.utcfromtimestamp(mktime(feed.updated_parsed))

        return (
            feed.updated_parsed is not None
            and self.feed_model.last_update < pytz.utc.localize(feed_updated_parsed)
        )


class FeedFetcher:
    def __init__(self, url):
        self.url = url

    def fetch(self):
        try:
            scraper = FeedScraper(url=self.url)
            scraper_feed, scraper_entries = scraper.scrap()
            defaults = {
                "title": scraper_feed.title,
                "link": scraper_feed.link,
                "published": scraper_feed.published_datetime,
                "last_update": scraper_feed.updated_datetime,
                "image": scraper_feed.image_url,
                "description": scraper_feed.description,
            }
            feed, _ = FeedModel.objects.update_or_create(
                feed_url=self.url, defaults=defaults
            )
            for entry in scraper_entries:
                defaults = {
                    "feed": feed,
                    "title": entry.title,
                    "description": entry.title,
                    "link": entry.link,
                    "author": entry.author,
                    "published_at": datetime.utcfromtimestamp(
                        mktime(entry.published_parsed)
                    ),
                }
                FeedItem.objects.update_or_create(link=entry.link, defaults=defaults)
        except FeedException:
            pass
