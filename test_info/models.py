from django.db import models


# 입맛 검사 질문
class TasteTestQuestion(models.Model):
    taste_question = models.TextField()
    taste_question_category = models.CharField(max_length=50)
    taste_question_image = models.ImageField()

    def __str__(self):
        return self.taste_question


# 입맛 검사 답변
class TasteTestAnswer(models.Model):
    taste_question = models.ForeignKey(
        "test_info.TasteTestQuestion", on_delete=models.CASCADE
    )
    taste_answer = models.CharField(max_length=100)


# FTI 검사 질문
class FtiTestQuestion(models.Model):
    fti_question = models.TextField()
    fti_question_image = models.ImageField()

    def __str__(self):
        return self.fti_question


# FTI 검사 답변
class FtiTestAnswer(models.Model):
    fti_question = models.ForeignKey(
        "test_info.FtiTestQuestion", on_delete=models.CASCADE
    )
    fti_answer = models.TextField()
    fti_style = models.CharField(max_length=10)
