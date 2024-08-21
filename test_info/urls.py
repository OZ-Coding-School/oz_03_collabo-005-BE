from django.urls import path

from .views import FTITestQuestionListView, UserFTITestResultCreateView

urlpatterns = [
    path("", FTITestQuestionListView.as_view(), name="fti_question"),
    path("user/", UserFTITestResultCreateView.as_view(), name="user_fti_test_create"),
]
