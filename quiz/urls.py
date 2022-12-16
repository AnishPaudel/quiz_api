"""
Url mapping for the quiz app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from quiz import views

router = DefaultRouter()

router.register("quizs", views.QuizViewSet)

app_name = "quiz"

urlpatterns = [path("", include(router.urls))]
