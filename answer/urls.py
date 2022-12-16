"""
URL mapping for the user API
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from answer import views


router = DefaultRouter()

router.register("answers", views.StudentQuizAnswersViewSet)

app_name = "answer"
# print("revers", router.urls)
urlpatterns = [
    path(
        "",
        include(router.urls),
    )
]
