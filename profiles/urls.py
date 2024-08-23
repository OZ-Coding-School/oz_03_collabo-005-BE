from django.urls import path

from .views import ProfileView, MyMeetingHistoryView

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("meeting/history/", MyMeetingHistoryView.as_view(), name="meeting_history")
]
