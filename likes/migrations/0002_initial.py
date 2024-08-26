# Generated by Django 4.2 on 2024-08-26 03:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("likes", "0001_initial"),
        ("reviews", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="reviewlike",
            name="review",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="review_like",
                to="reviews.review",
            ),
        ),
    ]
