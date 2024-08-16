from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
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


admin.site.register(CustomUser, CustomUserAdmin)
