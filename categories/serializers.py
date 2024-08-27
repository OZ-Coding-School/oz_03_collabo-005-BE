from rest_framework import serializers

from .models import Location, TimeSortCategory


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
