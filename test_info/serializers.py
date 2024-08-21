from django.db import models
from rest_framework import serializers

from .models import FTITestQuestion, FTITestResult


class FTITestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTITestQuestion
        fields = ("fti_question",)


class UserFTITestResultSerializer(serializers.Serializer):
    fti_style = serializers.ListField(
        child=serializers.CharField(max_length=3),
    )


