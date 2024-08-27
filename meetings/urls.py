from django.urls import path

from .views import (
    DeleteMeetingMemberView,
    FilterMeetingListView,
    JoinMeetingView,
    MeetingCreateView,
    MeetingDetailView,
    MeetingListView,
)

urlpatterns = [
    path("", MeetingListView.as_view(), name="meetings"),
    path("filter/", FilterMeetingListView.as_view(), name="filter_meetings"),
    path("<uuid:uuid>/", MeetingDetailView.as_view(), name="meeting_detail"),
    path("join/", JoinMeetingView.as_view(), name="join_meeting"),
    path("create/", MeetingCreateView.as_view(), name="create_meeting"),
    path(
        "delete/member/",
        DeleteMeetingMemberView.as_view(),
        name="delete_meeting_member",
    ),
]
