from django.db import IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from meetings.models import Meeting
from reviews.models import Review

from .models import MeetingLike, ReviewLike
from .serializers import LikeSerializer


# 좋아요 기능
class LikeView(APIView):
    serializer_class = LikeSerializer

    @extend_schema(tags=["Likes"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

            user = request.user
            uuid = request.data["uuid"]

            """
            UUID가 번개에 존재하는 경우, 번개의 좋아요
            UUID가 리뷰에 존재하는 경우, 리뷰의 좋아요 
            UUID가 존재하지 않는다면 NotFound
            """

            if Meeting.objects.filter(uuid=uuid).exists():
                meeting = Meeting.objects.get(uuid=uuid)

                MeetingLike.objects.create(user=user, meeting=meeting)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            elif Review.objects.filter(uuid=uuid).exists():
                review = Review.objects.get(uuid=uuid)

                ReviewLike.objects.create(user=user, review=review)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response(NotFound, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response(
                {"detail": "This is already liked post"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 좋아요 삭제
class DeleteLikeView(APIView):

    serializer_class = LikeSerializer

    @extend_schema(tags=["Likes"])
    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        """
        UUID가 번개에 존재하는 경우, 번개의 좋아요 삭제
        UUID가 리뷰에 존재하는 경우, 리뷰의 좋아요 삭제
        UUID가 존재하지 않는다면 NotFound
        """

        user = request.user
        uuid = request.data["uuid"]

        meeting = Meeting.objects.filter(uuid=uuid).first()

        if meeting:
            MeetingLike.objects.get(meeting=meeting, user=user).delete()
            return Response({"detail": "delete success"}, status=status.HTTP_200_OK)

        review = Review.objects.filter(uuid=uuid).first()

        if review:
            ReviewLike.objects.get(review=review, user=user).delete()
            return Response({"detail": "delete success"}, status=status.HTTP_200_OK)

        return Response({"detail": "delete failed"}, status=status.HTTP_404_NOT_FOUND)
