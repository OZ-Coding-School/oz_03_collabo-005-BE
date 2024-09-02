from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from comments.models import ReviewComment
from meetings.models import Meeting
from reviews.models import Review
from users.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    fti_type_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "nickname",
            "profile_image_url",
            "introduction",
            "fti_type",
            "fti_type_name",
            "spicy_preference",
        )

    @extend_schema_field(serializers.CharField)
    def get_fti_type_name(self, obj):
        return getattr(obj.fti_type, "fti_type", "")


class CreateProfileSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            "nickname",
            "profile_image_url",
            "introduction",
        )


class AnotherProfileSerializer(serializers.ModelSerializer):
    fti_type_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "nickname",
            "profile_image_url",
            "introduction",
            "fti_type",
            "fti_type_name",
        )

    @extend_schema_field(serializers.CharField)
    def get_fti_type_name(self, obj):
        return getattr(obj.fti_type, "fti_type", "")


class UserMeetingSerializer(serializers.ModelSerializer):
    payment_method_name = serializers.SerializerMethodField()
    age_group_name = serializers.SerializerMethodField()
    gender_group_name = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = (
            "uuid",
            "title",
            "payment_method",
            "payment_method_name",
            "age_group",
            "age_group_name",
            "gender_group",
            "gender_group_name",
            "meeting_time",
            "meeting_image_url",
            "description",
        )

    @extend_schema_field(serializers.CharField)
    def get_payment_method_name(self, obj):
        return obj.payment_method.payment_method

    @extend_schema_field(serializers.CharField)
    def get_age_group_name(self, obj):
        return obj.age_group.age_group

    @extend_schema_field(serializers.CharField)
    def get_gender_group_name(self, obj):
        return obj.gender_group.gender_group


class UserReviewSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            "uuid",
            "title",
            "category",
            "category_name",
            "content",
            "review_image_url",
            "hits",
            "comment_count",
            "created_at",
        )

    @extend_schema_field(serializers.IntegerField)
    def get_comment_count(self, obj):
        return ReviewComment.objects.filter(review=obj).count()

    @extend_schema_field(serializers.CharField)
    def get_category_name(self, obj):
        return obj.category.category
