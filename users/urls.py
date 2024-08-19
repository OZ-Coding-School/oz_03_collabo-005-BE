from django.urls import path

from .views import CustomUserSignUpView

urlpatterns = [
    path("signup/", CustomUserSignUpView.as_view(), name="signup"),
]
