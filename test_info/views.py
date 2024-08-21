import uuid
from collections import Counter

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.models import FTIType
from users.models import CustomUser

from .models import FTITestQuestion, FTITestResult
from .serializers import (
    FTITestQuestionSerializer,
    FTITestResultSerializer,
    UserFTITestResultSerializer, UserTasteTestQuestionSerializer,
)


class FTITestResultView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = FTITestResultSerializer

    @extend_schema(tags=["Fti_test"])
    def get(self, request, uuid):
        try:
            test_result = FTITestResult.objects.get(uuid=uuid)
        except FTITestResult.DoesNotExist:
            return Response(
                {"error": "Test result not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(instance=test_result)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 비로그인 유저와 로그인 유저의 테스트 결과를 저장
class FTITestResultCreateView(APIView):
    serializer_class = UserFTITestResultSerializer
    permission_classes = (AllowAny,)

    @extend_schema(tags=["Fti_test"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        selected_answer = serializer.validated_data["fti_style"]

        """
        Counter 객체에 리스트를 parameter로 담아주면
        dict 형태로 반환
        f : 3 (개)
        t : 1 (개)
        i : 2 (개)
        """
        counter = Counter(selected_answer)

        # 외향성 테스트
        extroversion = "T" if counter["T"] > counter["I"] else "I"
        # 탐구성 테스트
        curiosity = "A" if counter["A"] > counter["C"] else "C"
        # 접근성 테스트
        accessibility = "D" if counter["D"] > counter["N"] else "N"
        # 테스트 결과 조합
        fti_type = f"{extroversion}{curiosity}{accessibility}"
        fti_type_obj = FTIType.objects.get(fti_type=fti_type)
        test_uuid = uuid.uuid4()
        FTITestResult.objects.create(uuid=test_uuid, fti_type=fti_type_obj)

        if request.user.is_authenticated:
            user = CustomUser.objects.get(id=request.user.id)
            user.fti_type = fti_type_obj
            user.save()

        return Response(
            {"fti_type": fti_type, "uuid": test_uuid}, status=status.HTTP_201_CREATED
        )


class FTITestQuestionListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = FTITestQuestionSerializer

    @extend_schema(tags=["Fti_test"])
    def get(self, request):
        questions = FTITestQuestion.objects.all()
        serializer = self.serializer_class(instance=questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Taste
class UserTasetTestQuestionListView(APIView):
    serializer_class = UserTasteTestQuestionSerializer

    @extend_schema(tags=["Taste Test"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        pass
