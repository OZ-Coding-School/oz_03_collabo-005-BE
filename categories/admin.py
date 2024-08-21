from django.contrib import admin
from .models import FTIType


@admin.register(FTIType)
class FTITypeAdmin(admin.ModelAdmin):
    pass
