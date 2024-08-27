from rest_framework.views import APIView
from .utils import calculate_weights


class FoodsRecommend(APIView):
    def post(self, request):
        user = request.user

        weights = calculate_weights(user)
