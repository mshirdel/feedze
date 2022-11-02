import json
from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from feed.models import FeedItem, Feed
from user.models import User


class AbstractFeedzeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()

        cls.username1 = "username"
        cls.password1 = "$password123$"
        cls.sample_user1 = User.objects.create_user(
            username=cls.username1,
            email="test@example.com",
            password=cls.password1,
        )
        cls.sample_user2 = User.objects.create_user(
            username="username2", email="test2@example.com", password="$password123$"
        )

        cls.feed = Feed.objects.create(
            title="feed1",
            feed_url="https://example.com/feed/",
            link="https://example.com",
        )
        for i in range(10):
            FeedItem.objects.create(
                feed_id=cls.feed.id,
                title=f"feed item title {i}",
                link=f"https://example.com/news/item_news{i}",
                published_at=datetime.now(),
            )

    @staticmethod
    def sign_in_user(
        client: APIClient, username: str, password: str
    ) -> (APIClient, User, str):
        data = {"username": username, "password": password}
        response = client.post(
            reverse("token-obtain-pair"),
            json.dumps(data),
            content_type="application/json",
        )
        access_token = response.json()["access"]
        refresh_token = response.json()["refresh"]
        user = User.objects.get(username=username)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        return client, user, refresh_token
