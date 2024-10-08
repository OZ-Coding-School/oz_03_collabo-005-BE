from django.urls import path

from .views import (
    UserTasetTestAnswerListView,
    UserTasetTestQuestionListView,
    UserTasteResultView,
    UserTasteTestListView,
)

urlpatterns = [
    path("questions/", UserTasetTestQuestionListView.as_view(), name="taste_questions"),
    path("answer/", UserTasetTestAnswerListView.as_view(), name="taste_questions"),
    path("questions_list/", UserTasteTestListView.as_view(), name="taste_test_list"),
    path("taste_result/", UserTasteResultView.as_view(), name="taste_test_list"),
]
