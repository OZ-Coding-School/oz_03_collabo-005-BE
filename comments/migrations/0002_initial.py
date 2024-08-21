# Generated by Django 4.2 on 2024-08-21 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("comments", "0001_initial"),
        ("reviews", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="reviewcomment",
            name="review",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="reviews.review"
            ),
        ),
    ]
