from rest_framework import serializers

from categories.models import FoodFilter

from .models import *


# 푸드 필터
class CategoryFoodFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodFilter
        fields = "__all__"


class FTITypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTIType
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = (
            "id",
            "location_name",
        )


class MeetingAgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingAgeGroup
        fields = "__all__"


class MeetingGenderGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingGenderGroup
        fields = "__all__"


class MeetingPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingPaymentMethod
        fields = "__all__"


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
