"""
User Stat tests  
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from user_stat import models

# Create your tests here.
USER_STAT_URL = reverse("user_stat:userstat-list")


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


def createUserStat(user, **params):
    default = {
        "over_all_score": 12.0,
        "correct": 100,
        "incorrect": 6,
        "total_score": 107,
    }
    default.update(**params)
    user_stat = models.UserStat.objects.create(user=user, **default)
    return user_stat


class PrivateUserStatTests(TestCase):
    """Test for autheticated API requests"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(
            email="user@example.com", password="test123", username="teststaff"
        )
        self.user.is_staff = True
        self.client.force_authenticate(self.user)

    def test_returns_user_stat(self):
        "returns user stat on request"
        user_stat = createUserStat(self.user)

        res = self.client.get(USER_STAT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data[0]["over_all_score"], user_stat.over_all_score
        )  # noqa
