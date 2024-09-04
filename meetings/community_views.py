from django.db import IntegrityError
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Meeting, MeetingMember
from .serializers import JoinMeetingMemberSerializer, MeetingMemberSerializer


# 미팅에 참여하기
class CreateMeetingMember(APIView):

    serializer_class = JoinMeetingMemberSerializer

    @extend_schema(tags=["MeetingMember"])
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        meeting = Meeting.objects.get(uuid=request.data["meeting_uuid"])
        user = request.user
        meeting_members = MeetingMember.objects.filter(meeting=meeting)

        # 미팅 멤버들을 직렬화
        meeting_members_serializer = MeetingMemberSerializer(
            instance=meeting_members, many=True
        )

        # 미팅 멤버의 숫자
        count_meeting_member = MeetingMember.objects.filter(
            meeting_id=meeting.id
        ).count()

        # 호스트인지 확인하고 호스트인 경우엔 가입 불가능
        if meeting.user == user:
            return Response(
                {"detail": "Host cannot be join"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 인원 제한 확인
        if count_meeting_member >= meeting.maximum:
            return Response(
                {"detail": "Meeting members are full"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # 미팅 멤버 생성하고 미팅 멤버들을 반환
            MeetingMember.objects.create(user=user, meeting=meeting)
            return Response(
                meeting_members_serializer.data, status=status.HTTP_201_CREATED
            )

        except IntegrityError:
            return Response(
                {"detail": "You are already a member of this meeting."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteMeetingMember(APIView):

    serializer_class = JoinMeetingMemberSerializer

    @extend_schema(tags=["MeetingMember"])
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        meeting = Meeting.objects.get(uuid=request.data["meeting_uuid"])
        meeting_members = MeetingMember.objects.filter(meeting=meeting)

        meeting_members_serializer = MeetingMemberSerializer(
            instance=meeting_members, many=True
        )

        try:
            MeetingMember.objects.get(meeting=meeting, user=user).delete()
            return Response(meeting_members_serializer.data, status=status.HTTP_200_OK)

        except MeetingMember.DoesNotExist:
            return Response({"detail": "Meeting member does not exist"})
