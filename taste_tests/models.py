from django.db import models

from common.models import CommonModel


class TasteTestQuestion(CommonModel):
    fti_question = models.TextField()
