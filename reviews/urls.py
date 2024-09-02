from rest_framework.urls import path

from .views import (
    FilterReviewListView,
    ReviewDetailCreateView,
    ReviewDetailView,
    ReviewListView,
)

urlpatterns = [
    path("", ReviewListView.as_view(), name="review_list"),
    path(
        "filter/<str:category_name>",
        FilterReviewListView.as_view(),
        name="filter_reviews",
    ),
    path("detail/<uuid:uuid>/", ReviewDetailView.as_view(), name="review_detail"),
    path("detail/create/", ReviewDetailCreateView.as_view(), name="review_detail_save"),
]
