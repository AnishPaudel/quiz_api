"""Database models for quiz"""


from django.db import models

from django.conf import settings


class QuizAnswersOption(models.Model):
    """Quiz answer option Model"""

    answer = models.CharField(max_length=255)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class QuizQuestion(models.Model):
    """Quiz question Model"""

    question = models.CharField(max_length=255)
    mark = models.FloatField(default=1.0)
    is_multi = models.BooleanField(default=False)
    options = models.ManyToManyField("QuizAnswersOption")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # noqa

    def __str__(self):
        return self.question


class Quiz(models.Model):
    """Quiz Base model"""

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # noqa
    name = models.CharField(max_length=255)
    discription = models.TextField(blank=True)
    questions = models.ManyToManyField("QuizQuestion")
    # could add time feature

    def __str__(self):
        return self.name
