from django.urls import path

from .views import (
    CustomUserCheckEmailView,
    CustomUserCheckNickView,
    CustomUserLoginView,
    CustomUserSignUpView,
)

urlpatterns = [
    path("signup/", CustomUserSignUpView.as_view(), name="signup"),
    path("login/", CustomUserLoginView.as_view(), name="login"),
    path("checkEmail/", CustomUserCheckEmailView.as_view(), name="check_email"),
    path("checkNickname/", CustomUserCheckNickView.as_view(), name="check_nick"),
]
