from datetime import timedelta, datetime
from time import localtime
from unittest.mock import patch, Mock

from django.test import TestCase
from django.utils import timezone

from feed.models import Feed
from feed.feed_manager import FeedUpdater
from scraper.domain.entry import Entry

from scraper.domain.feed import Feed as FeedScraper


def fake_feed(*args, **kwargs):
    feed = FeedScraper(
        title="fake feed title",
        link="https://example.com/feed/",
        published="Wed, 02 Nov 2022 07:36:46 +0000",
        published_parsed=localtime(datetime.now().timestamp()),
        updated="Wed, 02 Nov 2022 07:36:46 +0000",
        updated_parsed=localtime(datetime.now().timestamp()),
        image_url="",
        description="",
    )
    entries = []
    for i in range(3):
        e = Entry(
            title=f"fake feed item - {i}",
            link=f"https://example.com/feed/item_{i}",
            author="Artur",
            published="Wed, 02 Nov 2022 07:36:46 +0000",
            summary=f"Summary {i}",
            content=f"Content {i}",
            published_parsed=localtime(datetime.now().timestamp()),
        )
        entries.append(e)

    return feed, entries


class UpdaterTest(TestCase):
    @patch("scraper.feed_scrapper.FeedScraper.scrap", Mock(side_effect=fake_feed))
    def test_required_update(self):
        feed = Feed.objects.create(
            feed_url="rss.example.com",
            title="test feed",
            last_update=timezone.now() - timedelta(hours=2),
        )
        updater = FeedUpdater(feed)
        self.assertTrue(updater.update())

    @patch("scraper.feed_scrapper.FeedScraper.scrap", Mock(side_effect=fake_feed))
    def test_not_required_update(self):
        feed = Feed.objects.create(
            feed_url="rss.example.com",
            title="test feed",
            last_update=timezone.now(),
        )
        updater = FeedUpdater(feed)
        self.assertFalse(updater.update())
