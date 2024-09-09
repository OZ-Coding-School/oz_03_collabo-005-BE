import uuid
from collections import Counter

from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from categories.models import FTIType
from users.models import CustomUser

from .models import FTITestQuestion, FTITestResult, TasteTestAnswer, TasteTestQuestion
from .serializers import (
    FTITestQuestionSerializer,
    FTITestResultSerializer,
    UserFTITestResultSerializer,
    UserTasteTestAnswerSerializer,
    UserTasteTestQuestionSerializer,
    UserTasteTestResultSerializer,
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
# permission_classes가 권한 분배가 안되어서 FTITestResult와 API를 합치지 못하고 있음
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
        extroversion = "T" if counter["T"] > counter["A"] else "A"
        # 탐구성 테스트
        curiosity = "I" if counter["I"] > counter["C"] else "C"
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
            {
                "fti_type": fti_type,
                "uuid": test_uuid,
                "fti_image": fti_type_obj.fti_image_url,
                "description": fti_type_obj.description,
            },
            status=status.HTTP_201_CREATED,
        )


class FTITestQuestionListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = FTITestQuestionSerializer

    @extend_schema(tags=["Fti_test"])
    def get(self, request):
        questions = FTITestQuestion.objects.all().order_by("id")
        serializer = self.serializer_class(instance=questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Taste
# Taset Question
class UserTasetTestQuestionListView(APIView):
    serializer_class = UserTasteTestQuestionSerializer

    @extend_schema(
        tags=["Taste Test"], description="단순 질문 리스트만 반환, 사용하지 않음"
    )
    def get(self, request):
        questions = TasteTestQuestion.objects.all()
        serializer = self.serializer_class(instance=questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Taset Answer
class UserTasetTestAnswerListView(APIView):
    serializer_class = UserTasteTestAnswerSerializer

    @extend_schema(
        tags=["Taste Test"], description="단순 답변 리스트만 반환, 사용하지 않음"
    )
    def get(self, request):
        answers = TasteTestAnswer.objects.all()
        serializer = self.serializer_class(instance=answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Taste Question & Answer
class UserTasteTestListView(APIView):
    question_serializer_class = UserTasteTestQuestionSerializer
    answer_serializer_class = UserTasteTestAnswerSerializer

    # 스웨거에게 기본 시리얼라이저클래스를 반환
    def get_serializer_class(self):
        return self.question_serializer_class

    @extend_schema(tags=["Taste Test"])
    def get(self, request):
        # 질문과 보기 세트용
        question_answers = []

        # 질문 전부 로드
        questions = TasteTestQuestion.objects.all()

        # 한 질문씩 반복하며 해당 보기들 병합
        for question in questions:
            question_serializer = self.question_serializer_class(instance=question)

            # 질문에 해당하는 보기들 모두 로드
            answers = TasteTestAnswer.objects.filter(taste_question=question.id)
            answer_serializer = self.answer_serializer_class(answers, many=True)

            # 세트 구성
            question_answers.append(
                {
                    "question": question_serializer.data,
                    "answers": answer_serializer.data,
                }
            )

        return Response(question_answers, status=status.HTTP_200_OK)


# Taste Type Save
class UserTasteResultView(APIView):
    pass
    serializer_class = UserTasteTestResultSerializer

    @extend_schema(
        tags=["Taste Test"],
        examples=[
            OpenApiExample(
                "Example",
                value={
                    "spicy_preference": 1,
                    "intensity_preference": 1,
                    "oily_preference": 3,
                    "flour_rice_preference": 2,
                    "cost_preference": 3,
                    "spicy_weight": 2,
                    "cost_weight": 1,
                },
            )
        ],
    )
    def post(self, request):
        # user 정보 객체
        user = request.user
        # 입맛 정보 객체
        serializer = self.serializer_class(data=request.data)

        # 입맛 정보 검증
        if not serializer.is_valid():
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)

        # 검증데이터 선언
        taste = serializer.validated_data

        # user데이터에 입맛 정보 할당
        user.spicy_preference = taste["spicy_preference"]
        user.intensity_preference = taste["intensity_preference"]
        user.oily_preference = taste["oily_preference"]
        user.flour_rice_preference = taste["flour_rice_preference"]
        user.cost_preference = taste["cost_preference"]
        user.spicy_weight = taste["spicy_weight"]
        user.cost_weight = taste["cost_weight"]

        # user 데이터 저장
        user.save()

        return Response("Success", status=status.HTTP_200_OK)
