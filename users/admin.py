from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "nickname",
                    "profile_image",
                    "introduction",
                    "fti_type",
                    "taste_type",
                )
            },
        ),
    )

    list_display = ("email", "nickname")
    search_fields = ("email", "nickname")
    ordering = ("email",)
