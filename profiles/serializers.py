from rest_framework import serializers

from meetings.models import Meeting, MeetingMember
from reviews.models import Review
from users.models import CustomUser
from comments.models import ReviewComment


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "nickname",
            "profile_image_url",
            "introduction",
            "fti_type",
        )


class UserMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = (
            "uuid",
            "title",
            "payment_method",
            "age_group",
            "gender_group",
            "meeting_time",
            "meeting_image_url",
            "description",
        )


class UserReviewSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = (
            "uuid",
            "title",
            "category",
            "content",
            "review_image_url",
            "hits",
            "comment_count",
            "created_at",
        )

    def get_comment_count(self, obj):
        return ReviewComment.objects.filter(review=obj).count()
