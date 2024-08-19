from django.db import models

from common.models import CommonModel


class FtiType(models.Model):
    fti_type = models.CharField(max_length=30)


class TestResult(CommonModel):
    user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)
    fti_type = models.OneToOneField(
        "test_results.FtiType", on_delete=models.SET_NULL, null=True
    )
    description = models.CharField(max_length=255)
