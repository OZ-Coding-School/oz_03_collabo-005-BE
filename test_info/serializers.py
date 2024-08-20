from django.db import models
from rest_framework.serializers import ModelSerializer

from common.models import CommonModel

from .models import FTITestQuestion


class FTITestQuestionSerializer(ModelSerializer):
    class Meta:
        model = FTITestQuestion
        fields = ("fti_question",)


class FTITestResult(CommonModel):
    user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)
    fti_type = models.OneToOneField(
        "categories.FtiType", on_delete=models.SET_NULL, null=True
    )
    description = models.CharField(max_length=255)


class UserFTITestResultSerializer(ModelSerializer):
    class Meta:
        model = FTITestResult
        fields = ("user", "fti_type", "description")
