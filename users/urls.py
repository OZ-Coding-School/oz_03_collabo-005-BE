from django.urls import path

from .views import CustomUserSignUpView, CustomUserLoginView

urlpatterns = [
    path("signup/", CustomUserSignUpView.as_view(), name="signup"),
    path("login/", CustomUserLoginView.as_view(), name="login"),
]

