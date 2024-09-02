from django.urls import path

from .views import (
    DeleteMeetingMemberView,
    FilterMeetingListView,
    JoinMeetingMemberView,
    MeetingCreateView,
    MeetingDetailView,
    MeetingListView,
)

urlpatterns = [
    path("", MeetingListView.as_view(), name="meetings"),
    path(
        "filter/<str:location_category>/<str:time_category>",
        FilterMeetingListView.as_view(),
        name="filter_meetings",
    ),
    path("<uuid:uuid>/", MeetingDetailView.as_view(), name="meeting_detail"),
    path("member/", JoinMeetingMemberView.as_view(), name="join_meeting"),
    path("create/", MeetingCreateView.as_view(), name="create_meeting"),
    path(
        "delete/member/",
        DeleteMeetingMemberView.as_view(),
        name="delete_meeting_member",
    ),
]
