"""
Database models for quiz answers
"""
from django.db import models

from django.conf import settings

from quiz.models import QuizAnswersOption, QuizQuestion, Quiz


# student answer


class QuizStudentAnswerOption(models.Model):

    std_answer = models.ForeignKey(QuizAnswersOption, on_delete=models.CASCADE)


class QuizStudentAnswerItem(models.Model):
    """Quiz Student Answer Item model """

    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    options = models.ManyToManyField("QuizStudentAnswerOption")


class QuizStudentAnswer(models.Model):
    """Quiz Student Answer"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answers = models.ManyToManyField("QuizStudentAnswerItem")
