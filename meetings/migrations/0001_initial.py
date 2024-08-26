# Generated by Django 4.2 on 2024-08-26 03:11

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Meeting",
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
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("title", models.CharField(max_length=150)),
                ("meeting_time", models.DateTimeField()),
                ("description", models.TextField()),
                ("meeting_image_url", models.URLField(null=True)),
                ("hits", models.PositiveIntegerField(default=0)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MeetingMember",
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
                ("is_host", models.BooleanField(default=False)),
                (
                    "meeting",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="meeting",
                        to="meetings.meeting",
                    ),
                ),
            ],
        ),
    ]
