import json

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.api_client = APIClient()
        self.user_name = "user1"
        self.user_pass = "#passwd123"
        self.user = User.objects.create_user(
            username=self.user_name, email="user1@example.com", password=self.user_pass
        )

    def login_user(self):
        payload = {"username": self.user_name, "password": self.user_pass}
        response = self.api_client.post(
            reverse("token-obtain-pair"),
            json.dumps(payload),
            content_type="application/json",
        )
        if response.status_code == status.HTTP_200_OK:
            access_token = response.json()["access"]
            refresh_token = response.json()["refresh"]
            return access_token, refresh_token

    def test_user_signup(self):
        payload = {
            "username": "username1",
            "email": "username1@example.com",
            "password": "#thepass$$",
            "password2": "#thepass$$",
        }
        response = self.api_client.post(
            reverse("user-signup"), json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_sign_in(self):
        payload = {"username": self.user_name, "password": self.user_pass}
        response = self.api_client.post(
            reverse("token-obtain-pair"),
            json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        _, refresh = self.login_user()
        payload = {"refresh": refresh}
        response = self.api_client.post(
            reverse("token-refresh"),
            json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("access" in response.data)
