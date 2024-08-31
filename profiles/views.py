from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import ReviewComment
from likes.models import ReviewLike
from meetings.models import Meeting, MeetingLike, MeetingMember
from reviews.models import Review
from users.models import CustomUser

from .serializers import (
    AnotherProfileSerializer,
    ProfileSerializer,
    CreateProfileSerializer,
    UserMeetingSerializer,
    UserReviewSerializer,
)


# 유저의 프로필 조회
class ProfileView(APIView):

    @extend_schema(
        tags=["profile"],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="ProfileResponse",
                    fields={
                        "profile": ProfileSerializer()
                    }
                )
            )
        },
    )
    def get(self, request):
        try:
            profile = CustomUser.objects.get(id=request.user.id)

        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(instance=profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["profile"],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="CreateProfileResponse",
                    fields={
                        "profile": CreateProfileSerializer()
                    }
                )
            )
        },
    )
    def post(self, request):
        user = request.user
        serializer = CreateProfileSerializer(instance=user, data=request.data)

        # 데이터 유효성
        if not serializer.is_valid():
            raise ValidationError("Invalid data")

        # 닉네임 중복 확인
        updated_nickname = serializer.validated_data.get("nickname")
        if (
            CustomUser.objects.filter(nickname=updated_nickname)
            .exclude(id=user.id)
            .exists()
        ):
            return Response(
                {"detail": "Nickname already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


# 내가 호스트인 번개 내역 조회
class UserHostedMeetingView(APIView):
    serializer_class = UserMeetingSerializer

    @extend_schema(tags=["profile"])
    def get(self, request):
        user = request.user
        hosted_meeting_ids = MeetingMember.objects.filter(
            user=user, is_host=True
        ).values_list("meeting_id", flat=True)
        hosted_meeting = Meeting.objects.filter(id__in=hosted_meeting_ids).order_by("-created_at")

        serializer = self.serializer_class(instance=hosted_meeting, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 내가 멤버로 참여한 번개 내역 조회
class UserJoinedMeetingView(APIView):
    serializer_class = UserMeetingSerializer

    @extend_schema(tags=["profile"])
    def get(self, request):
        user = request.user
        joined_meeting_ids = MeetingMember.objects.filter(
            user=user, is_host=False
        ).values_list("meeting_id", flat=True)
        joined_meeting = Meeting.objects.filter(id__in=joined_meeting_ids)

        serializer = self.serializer_class(instance=joined_meeting, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 내가 좋아요 한 번개 내역 조회
class UserLikedMeetingView(APIView):
    serializer_class = UserMeetingSerializer

    @extend_schema(tags=["profile"])
    def get(self, request):
        user = request.user
        liked_meeting_ids = MeetingLike.objects.filter(user=user).values_list(
            "meeting_id", flat=True
        )
        like_meeting = Meeting.objects.filter(id__in=liked_meeting_ids)

        serializer = self.serializer_class(instance=like_meeting, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 내가 작성한 리뷰 조회
class UserHostedReviewView(APIView):
    serializer_class = UserReviewSerializer

    @extend_schema(tags=["profile"])
    def get(self, request):
        user = request.user
        hosted_review_ids = Review.objects.filter(user=user, is_host=True).values_list(
            "id", flat=True
        )
        hosted_review = Review.objects.filter(id__in=hosted_review_ids)

        serializer = self.serializer_class(instance=hosted_review, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 내가 작성한 댓글이 달린 리뷰 조회
class UserCommentedReviewView(APIView):
    serializer_class = UserReviewSerializer

    @extend_schema(tags=["profile"])
    def get(self, request):
        user = request.user
        commented_review_ids = ReviewComment.objects.filter(user=user).values_list(
            "review_id", flat=True
        )
        commented_review = Review.objects.filter(id__in=commented_review_ids)

        serializer = self.serializer_class(instance=commented_review, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 내가 좋아요 한 리뷰 조회
class UserLikedReviewView(APIView):
    serializer_class = UserReviewSerializer

    @extend_schema(tags=["profile"])
    def get(self, request):
        user = request.user
        liked_review_ids = ReviewLike.objects.filter(user=user).values_list(
            "review_id", flat=True
        )
        liked_review = Review.objects.filter(id__in=liked_review_ids)

        serializer = self.serializer_class(instance=liked_review, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 다른 사람의 프로필 조회
class AnotherProfileView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AnotherProfileSerializer

    def get(self, request, nickname):
        nickname = nickname

        try:
            selected_user = CustomUser.objects.get(nickname=nickname)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "user is not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(instance=selected_user)

        return Response(serializer.data, status=status.HTTP_200_OK)
