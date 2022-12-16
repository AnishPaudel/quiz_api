"""Serializer for user stat """

from rest_framework import serializers
from user_stat.models import UserStat


class UserStatSerilizer(serializers.ModelSerializer):
    class Meta:
        model = UserStat
        fields = ["over_all_score", "total_score", "correct", "incorrect"]
