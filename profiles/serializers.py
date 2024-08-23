from rest_framework import serializers

from users.models import CustomUser
from meetings.models import Meeting


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
