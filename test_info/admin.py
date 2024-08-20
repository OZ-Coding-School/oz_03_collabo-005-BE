from django.contrib import admin

from .models import FtiTestAnswer, FtiTestQuestion, TasteTestAnswer, TasteTestQuestion


@admin.register(FtiTestQuestion)
class FTITestQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(FtiTestAnswer)
class FTITestAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(TasteTestQuestion)
class TasteTestQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(TasteTestAnswer)
class TasteTestAnswerAdmin(admin.ModelAdmin):
    pass
