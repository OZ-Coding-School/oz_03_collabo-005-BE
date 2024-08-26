from django.urls import path

from .views import FoodFilterList

urlpatterns = [
    #Food Filter
    path("foodfilter/", FoodFilterList.as_view(), name="FoodFilterList"),
]
