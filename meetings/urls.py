from django.urls import path

from .community_views import CreateMeetingMember, DeleteMeetingMember
from .views import (
    FilterMeetingListView,
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
    path("create/", MeetingCreateView.as_view(), name="create_meeting"),
    path("member/", CreateMeetingMember.as_view(), name="join_meeting_member"),
    path("member/delete/", DeleteMeetingMember.as_view(), name="delete_meeting_member"),
]
