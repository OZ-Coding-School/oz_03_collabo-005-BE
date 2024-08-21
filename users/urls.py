from django.urls import path

from .views import CustomUserLoginView, CustomUserSignUpView

urlpatterns = [
    path("signup/", CustomUserSignUpView.as_view(), name="signup"),
    path("login/", CustomUserLoginView.as_view(), name="login"),
]
