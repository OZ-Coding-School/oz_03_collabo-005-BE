# Generated by Django 4.2 on 2024-08-21 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("test_info", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tastetestanswer",
            name="taste_score",
            field=models.PositiveIntegerField(),
        ),
    ]
