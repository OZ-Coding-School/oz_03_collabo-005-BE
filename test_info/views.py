from collections import Counter

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FTITestQuestion
from .serializers import FTITestQuestionSerializer, UserFTITestResultSerializer


# 로그인한 유저의 테스트 결과를 저장
class UserFTITestResultCreateView(APIView):
    serializer_class = UserFTITestResultSerializer

    @extend_schema(tags=["Fti_test"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
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
        fti_type = f"{extroversion}{curiosity}{accessibility}"

        # User 모델의 fti_type 필드에 저장
        user.fti_type = fti_type
        user.save()

        return Response({"fti_type": fti_type}, status=status.HTTP_201_CREATED)


# FTI질문 리스트 조회
class FTITestQuestionListView(APIView):
    serializer_class = FTITestQuestionSerializer
    permission_classes = (AllowAny,)

    @extend_schema(tags=["Fti_test"])
    def get(self, request):
        questions = FTITestQuestion.objects.all()
        serializer = FTITestQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
