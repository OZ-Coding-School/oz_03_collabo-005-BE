from rest_framework.urls import path

from .views import (
    CreateReviewCommentView,
    ReviewCommentDeleteView,
    ReviewCommentUpdateView,
)

urlpatterns = [
    path("review/", CreateReviewCommentView.as_view(), name="review_comment"),
    path(
        "review/update/",
        ReviewCommentUpdateView.as_view(),
        name="review_comment_update",
    ),
    path(
        "review/delete/",
        ReviewCommentDeleteView.as_view(),
        name="review_comment_delete",
    ),
]
