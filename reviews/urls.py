from rest_framework.urls import path
from .views import ReviewListView


urlpatterns = [
    path("", ReviewListView.as_view(), name="review_list")
]
