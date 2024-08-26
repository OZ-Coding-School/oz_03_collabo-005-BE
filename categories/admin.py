from django.contrib import admin

from .models import (
    FoodFilter,
    FTIType,
    Location,
    MeetingAgeGroup,
    MeetingGenderGroup,
    MeetingPaymentMethod,
    ReviewCategory,
)


@admin.register(FTIType)
class FTITypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(ReviewCategory)
class ReviewCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(MeetingAgeGroup)
class MeetingAgeGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(MeetingPaymentMethod)
class MeetingPaymentMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(MeetingGenderGroup)
class MeetingGenderGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(FoodFilter)
class FoodFilterAdmin(admin.ModelAdmin):
    pass
