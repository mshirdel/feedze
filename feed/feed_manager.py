from datetime import datetime
from time import mktime

from scraper.domain.feed import Feed
from scraper.exceptions import FeedException
from scraper.feed_scrapper import FeedScraper
from feed.models import Feed as FeedModel, FeedItem


class FeedUpdater:
    def __init__(self, feed: FeedModel):
        self.feed_model = feed

    def update(self) -> bool:
        scraper = FeedScraper(url=self.feed_model.feed_url)
        scraper.scrap()
        if not self._check_for_update(scraper.feed):
            return False
        for entry in scraper.entries:
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
        import pytz

        feed_updated_parsed = datetime.utcfromtimestamp(mktime(feed.updated_parsed))

        return (
            feed.updated_parsed is not None
            and self.feed_model.last_update >= pytz.utc.localize(feed_updated_parsed)
        )


class FeedFetcher:
    def __init__(self, url):
        try:
            scraper = FeedScraper(url=url)
            scraper.scrap()
            defaults = {
                "title": scraper.feed.title,
                "link": scraper.feed.link,
                "published": scraper.feed.published_datetime,
                "last_update": scraper.feed.updated_datetime,
                "image": scraper.feed.image_url,
                "description": scraper.feed.description,
            }
            feed, _ = FeedModel.objects.update_or_create(
                feed_url=url, defaults=defaults
            )
            for entry in scraper.entries:
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
