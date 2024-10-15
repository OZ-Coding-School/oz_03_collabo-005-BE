from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from categories.models import FTIType
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
    good_relation = serializers.SerializerMethodField()
    good_reason = serializers.SerializerMethodField()
    good_relation_img = serializers.SerializerMethodField()
    bad_relation = serializers.SerializerMethodField()
    bad_reason = serializers.SerializerMethodField()
    bad_relation_img = serializers.SerializerMethodField()

    class Meta:

        model = FTITestResult
        fields = (
            "uuid",
            "fti_type",
            "description",
            "good_relation",
            "good_reason",
            "good_relation_img",
            "bad_relation",
            "bad_reason",
            "bad_relation_img",
            "fti_image_url",
        )

    @extend_schema_field(serializers.CharField)
    def get_description(self, obj):
        return obj.fti_type.description

    @extend_schema_field(serializers.URLField)
    def get_fti_image_url(self, obj):
        return obj.fti_type.fti_image_url

    @extend_schema_field(serializers.CharField)
    def get_good_relation(self, obj):
        return obj.fti_type.good_relation

    @extend_schema_field(serializers.CharField)
    def get_good_reason(self, obj):
        return obj.fti_type.good_reason

    @extend_schema_field(serializers.CharField)
    def get_bad_relation(self, obj):
        return obj.fti_type.bad_relation

    @extend_schema_field(serializers.CharField)
    def get_bad_reason(self, obj):
        return obj.fti_type.bad_reason

    @extend_schema_field(serializers.URLField)
    def get_good_relation_img(self, obj):
        img_name = obj.fti_type.good_relation
        try:
            img = FTIType.objects.get(fti_type=img_name).fti_image_url
        except FTIType.DoesNotExist:
            raise NotFound
        return img

    @extend_schema_field(serializers.URLField)
    def get_bad_relation_img(self, obj):
        img_name = obj.fti_type.bad_relation
        try:
            img = FTIType.objects.get(fti_type=img_name).fti_image_url
        except FTIType.DoesNotExist:
            raise NotFound
        return img




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
