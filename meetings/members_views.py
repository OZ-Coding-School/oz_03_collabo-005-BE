from http.client import responses
from wsgiref.util import request_uri

from django.db import IntegrityError
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import MeetingComment

from .models import Meeting, MeetingMember
from .serializers import (
    JoinMeetingMemberSerializer,
    MeetingCommentCreateSerializer,
    MeetingCommentDeleteSerializer,
    MeetingCommentSerializer,
    MeetingCommentUpdateSerializer,
    MeetingMemberSerializer,
)


# 미팅에 참여하기
class CreateMeetingMemberView(APIView):

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


# 미팅 취소하기
class DeleteMeetingMemberView(APIView):

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


# 미팅 멤버인지 확인
class MeetingMemeberCheckView(APIView):

    serializer_class = JoinMeetingMemberSerializer

    @extend_schema(tags=["MeetingMember"])
    def get(self, request, meeting_uuid):
        try:
            user_id = request.user.id
            meeting = Meeting.objects.get(uuid=meeting_uuid)
            meeting_member = MeetingMember.objects.get(meeting=meeting, user_id=user_id)

        except (
            MeetingMember.DoesNotExist,
            Meeting.DoesNotExist,
        ):
            return Response(NotFound, status.HTTP_404_NOT_FOUND)

        if user_id != meeting_member.user_id:
            return Response(
                {"detail": "Member NotFound", "result": False},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response({"result": True}, status.HTTP_200_OK)


# 소통방 댓글 로드
class MeetingCommentsView(APIView):

    serializer_class = MeetingCommentSerializer

    @extend_schema(tags=["MeetingMember"])
    def get(self, request, meeting_uuid):
        try:
            meeting = Meeting.objects.get(uuid=meeting_uuid)
            meeting_comments = MeetingComment.objects.filter(meeting=meeting)

        except Meeting.DoesNotExist:
            return Response(
                {"detail": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(instance=meeting_comments, context={"request": request}, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 소통방 댓글 등록
class MeetingCommentsCreateView(APIView):
    serializer_class = MeetingCommentCreateSerializer

    @extend_schema(tags=["MeetingMember"])
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            meeting = Meeting.objects.get(uuid=request.data["meeting_uuid"])

        except Meeting.DoesNotExist:
            return Response(
                {"detail": "Meeting not found"}, status=status.HTTP_404_NOT_FOUND
            )

        MeetingComment.objects.create(
            meeting=meeting,
            user=request.user,
            content=request.data["content"],
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 소통방 댓글 수정
class MeetingCommentUpdateView(APIView):

    serializer_class = MeetingCommentUpdateSerializer

    @extend_schema(tags=["MeetingMember"])
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            comment = MeetingComment.objects.get(id=request.data["comment_id"])
            user = request.user
            if user.id != comment.user.id:
                return Response({"It's not your Comment"}, status.HTTP_400_BAD_REQUEST)

            comment.content = request.data["content"]

            comment.save()

        except MeetingComment.DoesNotExist:
            return Response(
                {"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response({"detail": "update success"}, status=status.HTTP_200_OK)


# 소통방 댓글 삭제
class MeetingCommentDeleteView(APIView):

    serializer_class = MeetingCommentDeleteSerializer

    @extend_schema(tags=["MeetingMember"])
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            meeting_comment = MeetingComment.objects.get(id=request.data["comment_id"])
            user = request.user

            if user != meeting_comment.user:
                return Response({"It's not your Comment"}, status.HTTP_400_BAD_REQUEST)

        except MeetingComment.DoesNotExist:
            return Response(
                {"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        meeting_comment.delete()

        return Response({"detail": "Delete success"}, status=status.HTTP_200_OK)
