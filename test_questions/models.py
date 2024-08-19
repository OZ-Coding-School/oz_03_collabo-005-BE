from django.db import models

from common.models import CommonModel


class TasteTestQuestion(models.Model):
    taste_question = models.TextField()


class FtiTestQuestion(models.Model):
    fti_question = models.TextField()
