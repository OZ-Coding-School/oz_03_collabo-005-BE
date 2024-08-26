from rest_framework import serializers

from categories.models import FoodFilter


# 푸드 필터
class CategoryFoodFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodFilter
        fields = '__all__'