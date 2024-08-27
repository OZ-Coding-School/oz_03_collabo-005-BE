from rest_framework.urls import path
from .views import ReviewListView, ReviewDetailView


urlpatterns = [
    path("", ReviewListView.as_view(), name="review_list"),
    path("<uuid:uuid>/", ReviewDetailView.as_view(), name="review_detail")
]
