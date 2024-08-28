from django.urls import path

from .views import FoodsRecommend

urlpatterns = [
    path("recommends/", FoodsRecommend.as_view(), name="recommends"),
]
