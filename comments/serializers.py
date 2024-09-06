from rest_framework import serializers

from reviews.models import ReviewComment


class CreateReviewCommentSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = ReviewComment
        fields = (
            "uuid",
            "content",
        )


class UpdateReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = ("id", "content", "user_id")


class DeleteReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = ("id", "user_id")
