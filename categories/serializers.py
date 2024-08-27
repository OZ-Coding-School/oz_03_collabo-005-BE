from rest_framework import serializers

from .models import Location, TimeSortCategory, ReviewCategory


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


class ReviewCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewCategory
        fields = (
            "id",
            "category",
        )
