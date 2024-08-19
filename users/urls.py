from django.urls import path

from .views import CustomUserLoginView, CustomUserSignUpView, UserTestView

urlpatterns = [
    path("signup/", CustomUserSignUpView.as_view(), name="signup"),
    path("login/", CustomUserLoginView.as_view(), name="login"),
    # 투두 다른 API들로 정상동작 확인 후 삭제
    path("test/", UserTestView.as_view(), name="test"),
]
