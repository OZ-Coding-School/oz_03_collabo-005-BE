from collections import Counter

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FTITestQuestion, FTITestResult
from .serializers import FTITestQuestionSerializer, UserFTITestResultSerializer
import uuid

# 비로그인 유저와 로그인 유저의 테스트 결과를 저장
class UserFTITestResultCreateView(APIView):
    serializer_class = UserFTITestResultSerializer

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

        test_uuid = uuid.uuid4()
        FTITestResult.objects.create(
            uuid=test_uuid,
            fti_type_id=fti_type
        )

        if request.user.is_authenticated:
            user = request.user
            user.fti_type = fti_type
            user.save()

        return Response({"fti_type": fti_type, "uuid": test_uuid}, status=status.HTTP_201_CREATED)


class FTITestQuestionListView(APIView):
    @extend_schema(tags=["Fti_test"])
    def get(self, request):
        questions = FTITestQuestion.objects.all()
        serializer = FTITestQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
