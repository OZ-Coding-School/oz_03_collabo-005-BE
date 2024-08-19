# Generated by Django 4.2 on 2024-08-19 07:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FoodTag",
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
                ("food_tag", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Food",
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
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="생성일자"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="수정일자"),
                ),
                ("food_name", models.CharField(max_length=50)),
                (
                    "oil_preference",
                    models.PositiveIntegerField(
                        null=True, verbose_name=django.db.models.deletion.SET_NULL
                    ),
                ),
                (
                    "noodle_preference",
                    models.PositiveIntegerField(
                        null=True, verbose_name=django.db.models.deletion.SET_NULL
                    ),
                ),
                (
                    "rice_preference",
                    models.PositiveIntegerField(
                        null=True, verbose_name=django.db.models.deletion.SET_NULL
                    ),
                ),
                (
                    "spicy_preference",
                    models.PositiveIntegerField(
                        null=True, verbose_name=django.db.models.deletion.SET_NULL
                    ),
                ),
                (
                    "instant_preference",
                    models.PositiveIntegerField(
                        null=True, verbose_name=django.db.models.deletion.SET_NULL
                    ),
                ),
                (
                    "price_preference",
                    models.PositiveIntegerField(
                        null=True, verbose_name=django.db.models.deletion.SET_NULL
                    ),
                ),
                ("image_url", models.ImageField(upload_to="")),
                (
                    "food_tag",
                    models.ManyToManyField(related_name="foods", to="foods.foodtag"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]