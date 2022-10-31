from datetime import datetime
from time import mktime

from scraper.domain.feed import Feed
from scraper.feed_scrapper import FeedScraper
from feed.models import Feed as FeedModel, FeedItem


class FeedUpdater:
    def __init__(self, feed: FeedModel):
        self.feed_model = feed

    def update(self) -> bool:
        scraper = FeedScraper(url=self.feed_model.feed_url)
        if not self._check_for_update(scraper.feed):
            return False
        # self.feed_model.title = scraper.feed.title
        return True

    def _check_for_update(self, feed: Feed):
        return (
            feed.updated_parsed is not None
            and self.feed_model.last_update >= feed.updated_parsed
        )


class FeedFetcher:
    def __init__(self, url):
        scraper = FeedScraper(url=url)
        scraper.scrap()
        feed, _ = FeedModel.objects.get_or_create(
            feed_url=url,
            title=scraper.feed.title,
            link=scraper.feed.link,
            published=scraper.feed.published_datetime,
            last_update=scraper.feed.updated_datetime,
            image=scraper.feed.image_url,
        )
        for entry in scraper.entries:
            FeedItem.objects.get_or_create(
                feed=feed,
                title=entry.title,
                description=entry.title,
                link=entry.link,
                author=entry.author,
                published_at=datetime.utcfromtimestamp(mktime(entry.published_parsed)),
            )
