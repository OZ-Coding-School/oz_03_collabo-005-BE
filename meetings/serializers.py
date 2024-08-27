from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from meetings.models import Meeting, MeetingMember
from users.models import CustomUser


class MeetingListSerializer(serializers.ModelSerializer):
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
            "created_at",
        )


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
    @extend_schema_field(serializers.CharField)
    def get_nickname(self, obj):
        return obj.user.nickname


class MeetingMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "profile_image_url",
            "introduction",
        )


class JoinMeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingMember
        fields = (
            "meeting",
            "user",
            "is_host",
        )


class MeetingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = (
            "title",
            "location",
            "payment_method",
            "age_group",
            "gender_group",
            "meeting_time",
            "description",
            "meeting_image_url",
            "maximum",
        )


class DeleteMeetingMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingMember
        fields = ("meeting",)
