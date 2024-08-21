from django.urls import path

from .views import FTITestQuestionListView, FTITestResultCreateView, FTITestResultView

urlpatterns = [
    path("result/<uuid:uuid>", FTITestResultView.as_view(), name="fti_result_uuid"),
    path("question/", FTITestQuestionListView.as_view(), name="fti_questions"),
    path("result/", FTITestResultCreateView.as_view(), name="user_fti_test_create"),
]
