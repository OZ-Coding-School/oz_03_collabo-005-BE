from django.urls import path

from .views import FtiTestQuestionView

urlpatterns = [
    path("", FtiTestQuestionView.as_view(), name="fti_test_question"),
]
