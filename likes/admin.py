from django.contrib import admin

from .models import MeetingLike, ReviewLike


@admin.register(MeetingLike)
class MeetingLikeAdmin(admin.ModelAdmin):
    pass


@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    pass
