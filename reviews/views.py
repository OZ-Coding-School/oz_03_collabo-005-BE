from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework.permissions import AllowAny
from .models import Review
from categories.models import ReviewCategory
from .serializers import ReviewListSerializer, ReviewDetailSerializer
from categories.serializers import ReviewCategorySerializer
from rest_framework.response import Response
from rest_framework import status


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
    )
    def get(self, request):
        reviews = Review.objects.all().order_by("-created_at")
        review_categories = ReviewCategory.objects.all()

        reviews_data = ReviewListSerializer(reviews, many=True).data
        review_categories_data = ReviewCategorySerializer(review_categories, many=True).data

        review_list = {
            "reviews": reviews_data,
            "review_categories": review_categories_data,
        }

        return Response(review_list, status=status.HTTP_200_OK)


class ReviewDetailView(APIView):
    serializer_class = ReviewDetailSerializer

    @extend_schema(tags=["review"])
    def get(self, request, uuid):
        try:
            selected_review = Review.objects.get(uuid=uuid)

        except Review.DoesNotExist:
            raise NotFound("The review does not exist")
        serializer = self.serializer_class(instance=selected_review)

        # 게시물 조회 시 조회수 상승
        selected_review.hits += 1
        selected_review.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


