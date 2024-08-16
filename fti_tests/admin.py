from django.contrib import admin

from .models import FtiTestQuestion


@admin.register(FtiTestQuestion)
class FtiTestQuestionAdmin(admin.ModelAdmin):
    list_display = ("fti_question",)
    list_filter = ("fti_question",)
