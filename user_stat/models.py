"""Database models for user stat"""

from django.db import models
from django.conf import settings


class UserStat(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True
    )
    over_all_score = models.FloatField(default=0.0)
    total_score = models.IntegerField(default=0.0)
    correct = models.IntegerField(default=0.0)
    incorrect = models.IntegerField(default=0.0)
