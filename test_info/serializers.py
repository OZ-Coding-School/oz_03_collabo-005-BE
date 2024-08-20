from django.db import models
from rest_framework.serializers import ModelSerializer

from common.models import CommonModel

from .models import FtiTestQuestion


class FtiTestQuestionSerializer(ModelSerializer):
    class Meta:
        model = FtiTestQuestion
        fields = ("fti_question",)


class FtiType(models.Model):
    fti_type = models.CharField(max_length=30)


class TestResult(CommonModel):
    user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)
    fti_type = models.OneToOneField(
        "test_info.FtiType", on_delete=models.SET_NULL, null=True
    )
    description = models.CharField(max_length=255)


class UserFTITestResultSerializer(ModelSerializer):
    class Meta:
        model = TestResult
        field = ("user", "fti_type", "description")
