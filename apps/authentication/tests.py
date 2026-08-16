from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from apps.tests import CustomAPITestCase

User = get_user_model()


class LoginTests(CustomAPITestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("login")

    def test_login_success(self):
        response = self.client.post(
            self.url,
            {
                "username": "testuser",
                "password": "testuser123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Login successful.")

    def test_login_with_invalid_password(self):
        response = self.client.post(
            self.url,
            {
                "username": "testuser",
                "password": "wrong-password",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Invalid credentials.")

    def test_login_with_unknown_username(self):
        response = self.client.post(
            self.url,
            {
                "username": "unknown-user",
                "password": "TestPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_without_credentials(self):
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"],
            "Username and password are required.",
        )

    def test_login_requires_post(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
