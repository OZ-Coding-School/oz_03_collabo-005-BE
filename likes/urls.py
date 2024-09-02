from django.urls import path

from .views import DeleteLikeView, LikeView

urlpatterns = [
    path("", LikeView.as_view(), name="create_like"),
    path("delete/", DeleteLikeView.as_view(), name="delete_like"),
]
