from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from comments.models import MeetingComment
from meetings.models import Meeting
from users.models import CustomUser


class MeetingListSerializer(serializers.ModelSerializer):
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
            "created_at",
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


class MeetingDetailSerializer(serializers.ModelSerializer):
    nickname = serializers.SerializerMethodField()
    payment_method_name = serializers.SerializerMethodField()
    age_group_name = serializers.SerializerMethodField()
    gender_group_name = serializers.SerializerMethodField()

    class Meta:
        model = Meeting
        fields = (
            "uuid",
            "title",
            "nickname",
            "location",
            "payment_method",
            "payment_method_name",
            "age_group",
            "age_group_name",
            "gender_group",
            "gender_group_name",
            "meeting_time",
            "description",
            "meeting_image_url",
            "hits",
            "maximum",
            "likes_count",
            "created_at",
        )

    # Meeting 모델에서 user 필드를 참조하여 CustomUser의 nickname을 가져온다.
    # SerializerMethodField()를 사용하면 자동으로 obj 피라미터로 전달
    @extend_schema_field(serializers.CharField)
    def get_nickname(self, obj):
        return obj.user.nickname

    @extend_schema_field(serializers.CharField)
    def get_payment_method_name(self, obj):
        return obj.payment_method.payment_method

    @extend_schema_field(serializers.CharField)
    def get_age_group_name(self, obj):
        return obj.age_group.age_group

    @extend_schema_field(serializers.CharField)
    def get_gender_group_name(self, obj):
        return obj.gender_group.gender_group


class MeetingMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "profile_image_url",
            "introduction",
        )


class MeetingCreateSerializer(serializers.ModelSerializer):
    payment_method_name = serializers.CharField()
    age_group_name = serializers.CharField()
    gender_group_name = serializers.CharField()
    location_name = serializers.CharField()

    class Meta:
        model = Meeting
        fields = (
            "title",
            "location_name",
            "payment_method_name",
            "age_group_name",
            "gender_group_name",
            "meeting_time",
            "description",
            "meeting_image_url",
            "maximum",
        )



class MeetingUpdateSerializer(serializers.ModelSerializer):
    meeting_uuid = serializers.UUIDField()
    payment_method_name = serializers.CharField()
    age_group_name = serializers.CharField()
    gender_group_name = serializers.CharField()
    location_name = serializers.CharField()

    class Meta:
        model = Meeting
        fields = (
            "meeting_uuid",
            "title",
            "location_name",
            "payment_method_name",
            "age_group_name",
            "gender_group_name",
            "meeting_time",
            "description",
            "meeting_image_url",
            "maximum",
        )


class JoinMeetingMemberSerializer(serializers.Serializer):
    meeting_uuid = serializers.CharField()


class MeetingCommentSerializer(serializers.ModelSerializer):

    nickname = serializers.SerializerMethodField()
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = MeetingComment
        fields = (
            "id",
            "nickname",
            "profile_image_url",
            "content",
            "created_at",
        )

    @extend_schema_field(serializers.CharField)
    def get_nickname(self, obj):
        return obj.user.nickname

    @extend_schema_field(serializers.URLField)
    def get_profile_image_url(self, obj):
        return obj.user.profile_image_url


class MeetingCommentCreateSerializer(serializers.ModelSerializer):
    meeting_uuid = serializers.UUIDField()

    class Meta:
        model = MeetingComment
        fields = (
            "content",
            "meeting_uuid",
        )


class MeetingCommentUpdateSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
    content = serializers.CharField()


class MeetingCommentDeleteSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
