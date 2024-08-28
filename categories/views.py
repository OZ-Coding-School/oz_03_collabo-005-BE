from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FoodFilter
from .serializers import CategoryFoodFilterSerializer


class FoodFilterList(APIView):
    serializer_class = CategoryFoodFilterSerializer

    @extend_schema(tags=["Foods"])
    def get(self, request):
        # 필터 전부 로드
        categoryFilter = FoodFilter.objects.all()

        serializer = self.serializer_class(instance=categoryFilter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
