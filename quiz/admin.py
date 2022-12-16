from django.contrib import admin
from quiz.models import (
    Quiz,
    QuizAnswersOption,
    QuizQuestion,
)

# Register your models here.

admin.site.register(Quiz)
admin.site.register(QuizAnswersOption)
admin.site.register(QuizQuestion)
