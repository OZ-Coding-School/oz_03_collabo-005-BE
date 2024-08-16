from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fti_tests.models import FtiTestQuestion
from fti_tests.serializers import FtiTestQuestionSerializer


# FTI 질문 목록 조회
class FtiTestQuestionView(APIView):
    def get(self, request):
        questions = FtiTestQuestion.objects.all()

        serializer = FtiTestQuestionSerializer(questions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
