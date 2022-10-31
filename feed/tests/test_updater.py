from datetime import datetime, timedelta

from django.test import TestCase

from feed.models import Feed
from feed.feed_manager import FeedUpdater


class UpdaterTest(TestCase):
    def test_required_update(self):
        feed = Feed.objects.create(
            url="rss.example.com",
            title="test feed",
            last_update=datetime.now() - timedelta(hours=1),
        )
        updater = FeedUpdater(feed)
        self.assertTrue(updater.update())

    def test_not_required_update(self):
        feed = Feed.objects.create(
            url="rss.example.com",
            title="test feed",
            last_update=datetime.now() + timedelta(hours=1),
        )
        updater = FeedUpdater(feed)
        self.assertTrue(updater.update())
