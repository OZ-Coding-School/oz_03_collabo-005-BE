from django.urls import path

from .views import UserTasetTestQuestionListView

urlpatterns = [
    path("questions/", UserTasetTestQuestionListView.as_view(), name="taste_questions"),
]
