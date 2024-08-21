from django.urls import path

from common.views import *

urlpatterns = [
    path(
        "tasteQuestions/",
        BulkCreateTasteQuestionView.as_view(),
        name="BulkCreateTasteQeustion",
    ),
    path(
        "tasteAnswers/",
        BulkCreateTasteAnswerView.as_view(),
        name="BulkCreateTasteAnswer",
    ),
]
