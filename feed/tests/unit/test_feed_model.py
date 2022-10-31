from django.test import TestCase

from feed.models import Feed


class FeedModelTest(TestCase):
    def test_feed_create(self):
        url = "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml"
        new_feed = Feed.objects.create(feed_url=url)
        self.assertIsNotNone(new_feed)
