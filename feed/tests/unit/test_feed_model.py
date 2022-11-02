from datetime import datetime

from django.test import TestCase

from feed.models import Feed, FeedItem


class FeedModelTest(TestCase):
    def setUp(self) -> None:
        self.feed = Feed.objects.create(
            title="feed1",
            feed_url="https://example.com/feed/",
            link="https://example.com",
        )
        for i in range(10):
            FeedItem.objects.create(
                feed_id=self.feed.id,
                title=f"feed item title {i}",
                link=f"https://example.com/news/item_news{i}",
                published_at=datetime.now(),
            )

    def test_feed_create(self):
        self.assertIsNotNone(self.feed)
        self.assertEqual(self.feed.items.count(), 10)
