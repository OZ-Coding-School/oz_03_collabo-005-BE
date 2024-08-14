from django.contrib import  admin
from .models import CustomUser
from django.contrib.auth.models import User, Group


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["email", "nickname", "is_staff", "is_active", "created_at"]
    search_fields = ["email", "nickname"]


# admin 페이지에서 기본 User와 Group을 숨긴다.
admin.site.unregister(User)
admin.site.unregister(Group)