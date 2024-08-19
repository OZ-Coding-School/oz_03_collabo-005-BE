from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FtiTestQuestion
from .serializers import FtiTestQuestionSerializer


class FTITestQuestionListView(APIView):
    def get(self, request):
        serializer_class = FtiTestQuestionSerializer
        permission_classes = (AllowAny,)
        questions = FtiTestQuestion.objects.all()
        serializer = FtiTestQuestionSerializer(questions, many=True)
        return Response(serializer, status=status.HTTP_200_OK)
