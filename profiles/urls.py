from django.urls import path

from .views import (
    AnotherProfileView,
    ProfileUpdateView,
    ProfileView,
    UserCommentedReviewView,
    UserHostedMeetingView,
    UserHostedReviewView,
    UserJoinedMeetingView,
    UserLikedMeetingView,
    UserLikedReviewView,
)

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("update/", ProfileUpdateView.as_view(), name="profile_update"),
    path("hosted/meetings/", UserHostedMeetingView.as_view(), name="hosted_meeting"),
    path("joined/meetings/", UserJoinedMeetingView.as_view(), name="joined_meeting"),
    path("liked/meeting/", UserLikedMeetingView.as_view(), name="liked_meeting"),
    path("hosted/reviews/", UserHostedReviewView.as_view(), name="hosted_review"),
    path(
        "commented/reviews/", UserCommentedReviewView.as_view(), name="commented_review"
    ),
    path("liked/reviews/", UserLikedReviewView.as_view(), name="liked_review"),
    path("<str:nickname>/", AnotherProfileView.as_view(), name="another_profile"),
]
