from rest_framework import serializers

from categories.models import FoodFilter

from .models import Location, TimeSortCategory


# 푸드 필터
class CategoryFoodFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodFilter
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            "id",
            "location_name",
        )


class TimeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSortCategory
        fields = (
            "id",
            "sort_name",
        )
