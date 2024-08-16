from django.db import models


class FtiTestQuestion(models.Model):
    fti_question = models.CharField(max_length=200)
