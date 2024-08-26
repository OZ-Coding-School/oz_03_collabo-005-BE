from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from comments.models import ReviewComment
from likes.models import ReviewLike
from reviews.models import Review


class ReviewCommentSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    profile_img_url = serializers.SerializerMethodField()

    class Meta:
        model = ReviewComment
        fields = (
            "nickname",
            "profile_img_url",
            "created_at",
            "content",
        )

    @extend_schema_field(serializers.CharField)
    def get_nickname(self, obj):
        return obj.user.nickname

    @extend_schema_field(serializers.URLField)
    def get_profile_image_url(self, obj):
        return obj.user.profile_image_url


class ReviewDetailSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    comments = ReviewCommentSerializer(
        many=True, read_only=True, source="reviewcomment_set"
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
