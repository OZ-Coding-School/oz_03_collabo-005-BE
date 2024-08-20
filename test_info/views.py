from collections import Counter

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FtiTestQuestion
from .serializers import FtiTestQuestionSerializer, UserFTITestResultSerializer


# 로그인한 유저의 테스트 결과를 저장
class UserFTITestResultCreateView(APIView):
    serializer_class = UserFTITestResultSerializer

    @extend_schema(tags=["Fti_test"])
    def post(self, request):
        user = request.user
        selected_answer = request.data.get("fti_style")

        if not selected_answer:
            return Response(
                {"error": "No answers provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        """
        Counter 객체에 리스트를 parameter로 담아주면
        dict 형태로 변환해 준다.
        f : 3 (개)
        t : 1 (개)
        i : 2 (개)
        """
        counter = Counter(selected_answer)

        # 외향성 테스트
        if counter["T"] > counter["I"]:
            extroversion = "T"
        else:
            extroversion = "I"

        # 탐구성 테스트
        if counter["A"] > counter["C"]:
            curiosity = "A"
        else:
            curiosity = "C"

        # 접근성 테스트
        if counter["D"] > counter["N"]:
            accessibility = "D"
        else:
            accessibility = "N"

        groups = {
            "외향성": extroversion,
            "탐구성": curiosity,
            "접근성": accessibility,
        }

        # 결과 생성
        result = "".join(groups.values())

        # User 모델의 fti_type 필드를 업데이트
        user.fit_type = result
        user.save()

        return Response({"result": result}, status=status.HTTP_201_CREATED)


# FTI질문 리스트 조회
class FTITestQuestionListView(APIView):
    serializer_class = FtiTestQuestionSerializer
    permission_classes = (AllowAny,)

    @extend_schema(tags=["Fti_test"])
    def get(self, request):
        questions = FtiTestQuestion.objects.all()
        serializer = FtiTestQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
