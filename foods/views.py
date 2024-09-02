import numpy as np
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import calculate_weights, recommend_foods


class FoodsRecommend(APIView):
    @extend_schema(
        tags=["Recommend"],
        request={
            "application/json": {
                "type": "object",
                "data": {
                    "is_lunch": {"type": "boolean"},
                    "is_dinner": {"type": "boolean"},
                    "is_snack": {"type": "boolean"},
                    "is_date": {"type": "boolean"},
                    "is_party": {"type": "boolean"},
                    "is_diet": {"type": "boolean"},
                },
                "required": [
                    "is_lunch",
                    "is_dinner",
                    "is_snack",
                    "is_date",
                    "is_party",
                    "is_diet",
                ],
            }
        },
        examples=[
            OpenApiExample(
                name="Example",
                value={
                    "filters": {
                        "is_lunch": False,
                        "is_dinner": True,
                        "is_snack": True,
                        "is_date": False,
                        "is_party": True,
                        "is_diet": False,
                    },
                    "recommends_cnt": 5,
                },
            )
        ],
        responses={200: OpenApiResponse(description="Success")},
    )
    def post(self, request):
        user = request.user
        user_preferences = np.array(
            [
                user.oily_preference,
                user.flour_rice_preference,
                user.spicy_preference,
                user.intensity_preference,
                user.cost_preference,
            ]
        )
        filters = request.data.get("filters")
        recommends_cnt = request.data.get("recommends_cnt")

        weights = calculate_weights(
            user_preferences, user.spicy_weight, user.cost_weight
        )
        recommendations = recommend_foods(
            user_preferences, weights, filters, recommends_cnt
        )

        recommendations_list = []

        for i, (food, similarity) in enumerate(recommendations, 1):
            recommendations_list.append(
                {
                    "rank": i,
                    "food_name": food.food_name,
                    "food_id": food.id,
                    "spicy_preference": food.spicy_preference,
                    "intensity_preference": food.intensity_preference,
                    "oily_preference": food.oily_preference,
                    "flour_rice_preference": food.flour_rice_preference,
                    "cost_preference": food.cost_preference,
                    "spicy_weight": food.spicy_weight,
                    "cost_weight": food.cost_weight,
                    "image_url": food.image_url.url if food.image_url else None,
                    "is_lunch": food.is_lunch,
                    "is_dinner": food.is_dinner,
                    "is_snack": food.is_snack,
                    "is_date": food.is_date,
                    "is_party": food.is_party,
                    "is_diet": food.is_diet,
                }
            )

        print("\n추천 음식:")
        for i, (food, similarity) in enumerate(recommendations, 1):
            print(f"{i}. {food} (유사도: {similarity:.2f})")

        return Response({"status": "success", "recommendations": recommendations_list})
