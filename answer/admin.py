from django.contrib import admin
from answer import models

# Register your models here.
admin.site.register(models.QuizStudentAnswer)
admin.site.register(models.QuizStudentAnswerItem)
admin.site.register(models.QuizStudentAnswerOption)
