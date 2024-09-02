from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ReviewComment
from reviews.models import Review
from .serializers import CreateReviewCommentSerializer, UpdateReviewCommentSerializer, DeleteReviewCommentSerializer


class CreateReviewCommentView(APIView):
    serializer_class = CreateReviewCommentSerializer

    @extend_schema(tags=["comment"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        review = Review.objects.get(uuid=request.data["uuid"])
        content = serializer.data["content"]

        ReviewComment.objects.create(
            user=user,
            review=review,
            content=content,
        )

        return Response(serializer.data, status.HTTP_201_CREATED)


class ReviewCommentUpdateView(APIView):

    serializer_class = UpdateReviewCommentSerializer

    @extend_schema(tags=["comment"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            selected_comment = ReviewComment.objects.get(id=request.data["id"])

        except ReviewComment.DoesNotExist:
            return Response({"Comment don't exist"}, status.HTTP_400_BAD_REQUEST)

        selected_comment.content = request.data["content"]
        selected_comment.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewCommentDeleteView(APIView):
    serializer_class = DeleteReviewCommentSerializer

    @extend_schema(tags=["comment"])
    def post(self, request):
        try:
            selected_comment = ReviewComment.objects.get(id=request.data["id"])
            selected_comment.delete()

            return Response({"detail": "Delete successful"}, status=status.HTTP_200_OK)

        except ReviewComment.DoesNotExist:
            raise NotFound()
