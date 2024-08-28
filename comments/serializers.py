from rest_framework import serializers

from reviews.models import ReviewComment


class CreateReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = (
            "user",
            "review",
            "content",
        )


class UpdateReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = (
            "id",
            "user",
            "review",
            "content",
        )


class DeleteReviewCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewComment
        fields = ("id",)
