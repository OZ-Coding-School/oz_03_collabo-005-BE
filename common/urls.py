from django.urls import path

from .views import InputImage

urlpatterns = [
    path("image/", InputImage.as_view(), name="input_image"),
]
