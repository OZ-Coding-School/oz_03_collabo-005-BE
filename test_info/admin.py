from django.contrib import admin

from .models import FTITestAnswer, FTITestQuestion, TasteTestAnswer, TasteTestQuestion


@admin.register(FTITestQuestion)
class FTITestQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(FTITestAnswer)
class FTITestAnswerAdmin(admin.ModelAdmin):
    pass


@admin.register(TasteTestQuestion)
class TasteTestQuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(TasteTestAnswer)
class TasteTestAnswerAdmin(admin.ModelAdmin):
    pass
