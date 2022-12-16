"""
Views for user stat
"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from user_stat import serializer
from user_stat.models import UserStat


class UserStatViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """viewset for user stat"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = serializer.UserStatSerilizer
    queryset = UserStat.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
