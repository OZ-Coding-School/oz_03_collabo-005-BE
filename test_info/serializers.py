from rest_framework import serializers
from .models import TasteTestQuestion, TasteTestAnswer
from .models import FTITestQuestion, FTITestResult


class FTITestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTITestQuestion
        fields = ("fti_question",)


class UserFTITestResultSerializer(serializers.Serializer):
    fti_style = serializers.ListField(
        child=serializers.CharField(max_length=3),
    )


class FTITestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTITestResult
        fields = (
            "uuid",
            "fti_type",
        )


# TasetTestQuestion
class UserTasteTestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasteTestQuestion
        fields = "__all__"

# TasetTestQuestion
class UserTasteTestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasteTestAnswer
        fields = "__all__"

