# Generated by Django 4.2 on 2024-08-21 04:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FTITestQuestion",
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
                ("fti_question", models.TextField()),
                ("fti_question_image", models.ImageField(upload_to="")),
            ],
        ),
        migrations.CreateModel(
            name="TasteTestQuestion",
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
                ("taste_question", models.TextField()),
                ("taste_question_category", models.CharField(max_length=50)),
                (
                    "taste_question_image",
                    models.ImageField(default="abc.jpg", upload_to=""),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TasteTestAnswer",
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
                ("taste_answer", models.CharField(max_length=100)),
                ("taste_score", models.PositiveIntegerField(max_length=6)),
                (
                    "taste_question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test_info.tastetestquestion",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FTITestResult",
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
                ("uuid", models.CharField(max_length=100)),
                (
                    "fti_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="categories.ftitype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FTITestAnswer",
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
                ("fti_answer", models.TextField()),
                ("fti_style", models.CharField(max_length=10)),
                (
                    "fti_question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="test_info.ftitestquestion",
                    ),
                ),
            ],
        ),
    ]
