from django.urls import path

from .views import FTITestQuestionListView

urlpatterns = [path("", FTITestQuestionListView.as_view(), name="fti_question")]
