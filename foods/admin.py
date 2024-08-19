from django.contrib import admin

from .models import Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    field = (
        "food_name",
        "oil_preference",
        "noodle_preference",
        "rice_preference",
        "spicy_preference",
        "instant_preference",
        "price_preference",
        "image_url",
        "food_tag",
    )
