from django.urls import path

from .members_views import (
    CreateMeetingMemberView,
    DeleteMeetingMemberView,
    MeetingCommentDeleteView,
    MeetingCommentsCreateView,
    MeetingCommentsView,
    MeetingCommentUpdateView,
    MeetingMemeberCheckView,
)
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
    path("member/", CreateMeetingMemberView.as_view(), name="join_meeting_member"),
    path(
        "member/delete/",
        DeleteMeetingMemberView.as_view(),
        name="delete_meeting_member",
    ),
    path(
        "member/check/<uuid:meeting_uuid>/",
        MeetingMemeberCheckView.as_view(),
        name="meeting_member_check",
    ),
    path(
        "member/comments/<uuid:meeting_uuid>",
        MeetingCommentsView.as_view(),
        name="meeting_comments",
    ),
    path(
        "member/comment/create/",
        MeetingCommentsCreateView.as_view(),
        name="meeting_comment_create",
    ),
    path(
        "member/comment/delete/",
        MeetingCommentDeleteView.as_view(),
        name="meeting_comment_delete",
    ),
    path(
        "member/comment/update/",
        MeetingCommentUpdateView.as_view(),
        name="meeting_comment_update",
    ),
]
