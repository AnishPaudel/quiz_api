"""
Tests for the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:profile")


def create_user(username, password, email):
    user = get_user_model().objects.create(
        username=username, email=email, password=password
    )
    return user


class PublicUserApiTest(TestCase):
    """Test the public features of the user api"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_sucess(self):
        """Test creating a user is successfull"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "username": "test",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_email_exists_error(self):
        """Test error returned if user with email exists"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "username": "TestName",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            "email": "test@example.com",
            "password": "pw",
            "username": "Test name",
        }  # noqa
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = (
            get_user_model().objects.filter(email=payload["email"]).exists()
        )  # noqa
        self.assertFalse(user_exists)

    # def test_create_token_for_user(self):
    #     """Test generates token for valid credentials."""
    #     user_details = {
    #         "username": "test123",
    #         "email": "test1@example.com",
    #         "password": "testpass",
    #     }
    #     user = create_user(**user_details)
    #     print(user, user.get_username(), user.email, "2233")
    #     payload = {
    #         "username": user_details["username"],
    #         "password": user_details["password"],
    #     }  # noqa

    #     res = self.client.post(TOKEN_URL, payload)
    #     self.assertIn("token", res.data)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credintials(self):
        """Test return error if credentials invalid"""
        create_user(
            email="test@example.com", password="goodpass", username="test"
        )  # noqa
        payload = {"email": "test@example.com", "password": "badpass"}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error"""
        payload = {
            "email": "test@example.com",
            "password": "",
            "username": "test",
        }  # noqa
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorized(self):
        """Test authentication is required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test APoi requests that require authenitcation."""

    def setUp(self):
        self.user = create_user(
            username="testname",
            email="test@example.com",
            password="testpass123",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retirve_profile_sucess(self):
        """Test retriveig profile for logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data, {"username": self.user.get_username(), "email": self.user.email}
        )  # noqa

    def test_post_me_not_allowed(self):
        """Test post is not allowed for the men endpoint"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {"username": "updatedname", "password": "newpassword123"}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.get_username(), payload["username"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
