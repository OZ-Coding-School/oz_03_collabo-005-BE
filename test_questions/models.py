from django.contrib.postgres.fields import ArrayField
from django.db import models

from common.models import CommonModel


class TasteTestQuestion(models.Model):
    taste_question = models.TextField()
    taste_answer = ArrayField(
        models.CharField(max_length=50),
        size=10,
        blank=True,
        null=True,
    )


class FtiTestQuestion(models.Model):
    fti_question = models.TextField()
