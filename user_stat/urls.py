"""
Url for user stat
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_stat import views


router = DefaultRouter()

router.register("user_stat", views.UserStatViewSet)

app_name = "user_stat"
# print("revers", router.urls)
urlpatterns = [
    path(
        "",
        include(router.urls),
    )
]
