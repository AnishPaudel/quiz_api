# Generated by Django 4.1 on 2022-12-14 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0006_quizquestion_creator"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizstudentanswer",
            name="quiz",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="quiz.quiz"
            ),
            preserve_default=False,
        ),
    ]
