from django.urls import path

from .views import *

urlpatterns = [
    # Food Filter
    path("foodfilter/", FoodFilterList.as_view(), name="FoodFilterList"),
    path("ftitypefiler/", FTITypeList.as_view(), name="FTITypeList"),
    path("locationfilter/", LocationList.as_view(), name="LocationList"),
    path("meetingagefilter/", MeetingAgeGroupList.as_view(), name="MeetingAgeGroupList"),
    path("meetinggenderfilter/", MeetingGenderGroupList.as_view(), name="MeetingGenderGroupList"),
    path("meetingpaymentfilter/", MeetingPaymentMethodList.as_view(), name="MeetingPaymentMethodList"),
    path("reviewfilter/", ReviewFilterList.as_view(), name="ReviewFilterList"),
    path("timesortfilter/", TimeSortFilterList.as_view(), name="TimeSortFilterList"),
]
