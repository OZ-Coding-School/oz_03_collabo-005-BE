from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.models import ReviewCategory
from categories.serializers import ReviewCategorySerializer
from comments.models import ReviewComment

from .models import Review
from .serializers import (
    CreateReviewSerializer,
    ReviewCommentSerializer,
    ReviewDetailSerializer,
    ReviewListSerializer,
)


# 리뷰 목록 조회
class ReviewListView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["review"],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="ReviewListResponse",
                    fields={
                        "reviews": ReviewListSerializer(many=True),
                        "review_categories": ReviewCategorySerializer(many=True),
                    },
                )
            )
        },
        operation_id="review_list",
    )
    def get(self, request):
        reviews = Review.objects.all().order_by("-created_at")
        review_categories = ReviewCategory.objects.all()

        reviews_data = ReviewListSerializer(reviews, many=True).data
        review_categories_data = ReviewCategorySerializer(
            review_categories, many=True
        ).data

        review_list = {
            "reviews": reviews_data,
            "review_categories": review_categories_data,
        }

        return Response(review_list, status=status.HTTP_200_OK)


# 필터링 된 리뷰 리스트 조회
class FilterReviewListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ReviewListSerializer

    @extend_schema(tags=["review"])
    def get(self, request):
        review_category_id = request.GET.get("review_category_id")
        reviews = Review.objects.filter(id=review_category_id)

        serializer = self.serializer_class(instance=reviews, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 리뷰 상세 조회
class ReviewDetailView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["review"],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="ReviewDetailResponse",
                    fields={
                        "review": ReviewDetailSerializer(),
                        "comments": ReviewCommentSerializer(many=True),
                    },
                )
            )
        },
        operation_id="review_detail",
    )
    def get(self, request, uuid):
        try:
            selected_review = Review.objects.get(uuid=uuid)
            review_data = ReviewDetailSerializer(instance=selected_review).data

        except Review.DoesNotExist:
            raise NotFound("The review does not exist")

        # 게시물 조회 시 조회수 상승
        selected_review.hits += 1
        selected_review.save()

        comments = ReviewComment.objects.filter(review_id=selected_review.id)
        comments_data = ReviewCommentSerializer(instance=comments, many=True).data

        review_detail = {
            "review": review_data,
            "comments": comments_data,
        }

        return Response(review_detail, status=status.HTTP_200_OK)


class ReviewDetailCreateView(APIView):
    serializer_class = CreateReviewSerializer

    @extend_schema(tags=["review"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        category = request.data["category"]
        title = request.data["title"]
        content = request.data["content"]
        review_image_url = request.data["review_image_url"]
        is_host = True

        Review.objects.create(
            user=user,
            category_id=category,
            title=title,
            content=content,
            review_image_url=review_image_url,
            is_host=is_host,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
