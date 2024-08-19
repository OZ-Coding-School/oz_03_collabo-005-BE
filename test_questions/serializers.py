from rest_framework.serializers import ModelSerializer

from .models import FtiTestQuestion


class FtiTestQuestionSerializer(ModelSerializer):
    class Meta:
        model = FtiTestQuestion
        fields = ("fti_question",)
