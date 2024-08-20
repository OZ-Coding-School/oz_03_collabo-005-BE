from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FtiTestQuestion
from .serializers import FtiTestQuestionSerializer, UserFTITestResultSerializer


# 로그인한 유저의 테스트 결과를 저장
class UserFTITestResultCreateView(APIView):
    serializer_class = UserFTITestResultSerializer
    permission_classes = IsAuthenticated

    @extend_schema(tags=["Fti_test"])
    def post(self, request):
        data = {
            "user": request.user.id,
        }


class FTITestQuestionListView(APIView):
    serializer_class = FtiTestQuestionSerializer
    permission_classes = (AllowAny,)

    @extend_schema(tags=["Fti_test"])
    def get(self, request):
        questions = FtiTestQuestion.objects.all()
        serializer = FtiTestQuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
