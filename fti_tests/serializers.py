from rest_framework import serializers

from fti_tests.models import FtiTestQuestion


class FtiTestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FtiTestQuestion
        fields = "__all__"
