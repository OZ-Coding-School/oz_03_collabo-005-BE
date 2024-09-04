from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *


class FoodFilterList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CategoryFoodFilterSerializer

    @extend_schema(tags=["Category"])
    def get(self, request):
        # 필터 전부 로드
        categoryFilter = FoodFilter.objects.all()

        serializer = self.serializer_class(instance=categoryFilter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FTITypeList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = FTITypeSerializer

    @extend_schema(tags=["Category"])
    def get(self, request):
        # 필터 전부 로드
        categoryFilter = FTIType.objects.all()

        serializer = self.serializer_class(instance=categoryFilter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocationList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LocationSerializer

    @extend_schema(tags=["Category"])
    def get(self, request):
        # 필터 전부 로드
        categoryFilter = Location.objects.all()

        serializer = self.serializer_class(instance=categoryFilter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MeetingAgeGroupList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = MeetingAgeGroupSerializer

    @extend_schema(tags=["Category"])
    def get(self, request):
        # 필터 전부 로드
        categoryFilter = MeetingAgeGroup.objects.all()

        serializer = self.serializer_class(instance=categoryFilter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MeetingGenderGroupList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = MeetingGenderGroupSerializer

    @extend_schema(tags=["Category"])
    def get(self, request):
        # 필터 전부 로드
        categoryFilter = MeetingGenderGroup.objects.all()

        serializer = self.serializer_class(instance=categoryFilter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MeetingPaymentMethodList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = MeetingPaymentMethodSerializer

    @extend_schema(tags=["Category"])
    def get(self, request):
        # 필터 전부 로드
        categoryFilter = MeetingPaymentMethod.objects.all()

        serializer = self.serializer_class(instance=categoryFilter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewFilterList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ReviewCategorySerializer

    @extend_schema(tags=["Category"])
    def get(self, request):
        # 필터 전부 로드
        categoryFilter = ReviewCategory.objects.all()

        serializer = self.serializer_class(instance=categoryFilter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TimeSortFilterList(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TimeCategorySerializer

    @extend_schema(tags=["Category"])
    def get(self, request):
        # 필터 전부 로드
        categoryFilter = TimeSortCategory.objects.all()

        serializer = self.serializer_class(instance=categoryFilter, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
