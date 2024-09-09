from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from users.models import CustomUser

from .models import FTITestQuestion, FTITestResult, TasteTestAnswer, TasteTestQuestion


class FTITestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTITestQuestion
        fields = (
            "fti_question",
            "fti_question_image",
        )


class UserFTITestResultSerializer(serializers.Serializer):
    fti_style = serializers.ListField(
        child=serializers.CharField(max_length=1),
    )


class FTITestResultSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    fti_image_url = serializers.SerializerMethodField()

    class Meta:

        model = FTITestResult
        fields = (
            "uuid",
            "fti_type",
            "description",
            "fti_image_url",
        )

    @extend_schema_field(serializers.CharField)
    def get_description(self, obj):
        return obj.fti_type.description

    @extend_schema_field(serializers.URLField)
    def get_fti_image_url(self, obj):
        return obj.fti_type.fti_image_url


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
