from django.contrib import admin

from .models import ReviewComment


@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    pass
