# Generated by Django 5.1.7 on 2025-04-07 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0018_userprofile_achievements_userprofile_education_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="achievements",
            field=models.TextField(default="", max_length=256),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="education",
            field=models.TextField(default="", max_length=256),
        ),
    ]
