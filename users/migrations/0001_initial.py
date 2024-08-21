# Generated by Django 4.2 on 2024-08-21 04:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("categories", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
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
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
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
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=255)),
                ("nickname", models.CharField(max_length=50, unique=True)),
                (
                    "profile_image",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_images/"
                    ),
                ),
                ("introduction", models.TextField(blank=True, null=True)),
                (
                    "spicy_preference",
                    models.PositiveIntegerField(default=None, null=True),
                ),
                (
                    "intensity_preference",
                    models.PositiveIntegerField(default=None, null=True),
                ),
                (
                    "oily_preference",
                    models.PositiveIntegerField(default=None, null=True),
                ),
                (
                    "flour_rice_preference",
                    models.PositiveIntegerField(default=None, null=True),
                ),
                (
                    "cost_preference",
                    models.PositiveIntegerField(default=None, null=True),
                ),
                ("spicy_weight", models.PositiveIntegerField(default=None, null=True)),
                ("cost_weight", models.PositiveIntegerField(default=None, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "fti_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="categories.ftitype",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
