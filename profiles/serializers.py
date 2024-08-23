from rest_framework import serializers

from meetings.models import Meeting
from users.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "nickname",
            "profile_image_url",
            "introduction",
            "fti_type",
        )


class MeetingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = (
            "title",
            "payment_method",
            "meeting_time",
            "description",
        )
