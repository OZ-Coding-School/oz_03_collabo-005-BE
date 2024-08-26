from rest_framework import serializers
from meetings.models import Meeting


class MeetingDetailSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = (
            "uuid",
            "title",
            "nickname",
            "location",
            "payment_method",
            "age_group",
            "gender_group",
            "meeting_time",
            "description",
            "meeting_image_url",
            "hits",
            "likes_count",
            "created_at",
        )

    # Meeting 모델에서 user 필드를 참조하여 CustomUser의 nickname을 가져온다.
    # SerializerMethodField()를 사용하면 자동으로 obj 피라미터로 전달
    def get_nickname(self, obj):
        return obj.user.nickname
