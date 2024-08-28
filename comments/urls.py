from rest_framework.urls import path

from .views import (
    CreateReviewCommentView,
    ReviewCommentDeleteView,
    ReviewCommentUpdateView,
)

urlpatterns = [
    path("comment/", CreateReviewCommentView.as_view(), name="review_comment"),
    path(
        "comment/update/",
        ReviewCommentUpdateView.as_view(),
        name="review_comment_update",
    ),
    path(
        "comment/delete/",
        ReviewCommentDeleteView.as_view(),
        name="review_comment_delete",
    ),
]
