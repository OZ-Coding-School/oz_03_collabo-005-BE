from django.contrib import admin
from .models import FtiTestQuestion


@admin.register(FtiTestQuestion)
class FTITestQuestionAdmin(admin.ModelAdmin):
    pass

