# Generated by Django 4.1 on 2022-12-11 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="quizanswer",
            name="answerJson",
            field=models.TextField(blank=True),
        ),
    ]
