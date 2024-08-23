from rest_framework import serializers

from users.models import CustomUser

from .models import FTITestQuestion, FTITestResult, TasteTestAnswer, TasteTestQuestion


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


# TasteTestQuestion
class UserTasteTestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasteTestQuestion
        fields = "__all__"


# TasteTestAnswer
class UserTasteTestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasteTestAnswer
        fields = "__all__"


# TasteTestResult
class UserTasteTestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "spicy_preference",
            "intensity_preference",
            "oily_preference",
            "flour_rice_preference",
            "cost_preference",
            "spicy_weight",
            "cost_weight",
        )
