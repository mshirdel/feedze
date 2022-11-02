from django.urls import reverse
from rest_framework import status

from feed.tests.abstract_test import AbstractFeedzeTest


class TestFeedModel(AbstractFeedzeTest):
    def test_creat_feed(self):
        client, _, _ = self.sign_in_user(
            self.api_client, self.username1, self.password1
        )
        url = reverse("feed-viewset-import-feed")
        response = client.post(url, data={"url": "https://www.digikala.com/mag/feed/"})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_add_new_follower(self):
        client, _, _ = self.sign_in_user(
            self.api_client, self.username1, self.password1
        )
        url = reverse("feed-viewset-follow", args=[self.feed.id])
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_remove_follower(self):
        client, _, _ = self.sign_in_user(
            self.api_client, self.username1, self.password1
        )
        url = reverse("feed-viewset-follow", args=[self.feed.id])
        response = client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
