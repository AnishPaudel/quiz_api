# Generated by Django 4.1 on 2022-12-14 16:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("quiz", "0002_alter_quizanswer_answerjson"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuizQuestion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question", models.CharField(max_length=255)),
                ("is_multi", models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameModel(
            old_name="QuizAnswer",
            new_name="QuizStudentAnswer",
        ),
        migrations.RemoveField(
            model_name="quizanswersoption",
            name="question",
        ),
        migrations.AddField(
            model_name="quizanswersoption",
            name="is_answer",
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name="QuizQuestions",
        ),
        migrations.AddField(
            model_name="quizquestion",
            name="options",
            field=models.ManyToManyField(to="quiz.quizanswersoption"),
        ),
        migrations.AddField(
            model_name="quiz",
            name="questions",
            field=models.ManyToManyField(to="quiz.quizquestion"),
        ),
    ]