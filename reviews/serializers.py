from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from comments.models import ReviewComment
from likes.models import ReviewLike
from reviews.models import Review


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "uuid",
            "user",
            "category",
            "title",
            "content",
            "hits",
            "review_image_url",
            "is_host",
            "created_at",
            "comment_count",
        )


class ReviewCommentSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = ReviewComment
        fields = (
            "nickname",
            "profile_image_url",
            "created_at",
            "content",
        )

    @extend_schema_field(serializers.CharField)
    def get_nickname(self, obj):
        reviewer = obj.user
        return reviewer.nickname

    @extend_schema_field(serializers.URLField)
    def get_profile_image_url(self, obj):
        reviewer = obj.user
        return reviewer.profile_image_url


class ReviewDetailSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    comments = ReviewCommentSerializer(
        many=True, read_only=True, source="review_comments"
    )

    class Meta:
        model = Review
        fields = (
            "uuid",
            "title",
            "category",
            "nickname",
            "content",
            "review_image_url",
            "hits",
            "comment_count",
            "likes_count",
            "created_at",
            "comments",
        )

    @extend_schema_field(serializers.IntegerField)
    def get_comment_count(self, obj):
        return ReviewComment.objects.filter(review=obj).count()

    @extend_schema_field(serializers.IntegerField)
    def get_likes_count(self, obj):
        return ReviewLike.objects.filter(review=obj).count()

    @extend_schema_field(serializers.CharField)
    def get_nickname(self, obj):
        return obj.user.nickname


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "title",
            "category",
            "content",
            "review_image_url",
        )
