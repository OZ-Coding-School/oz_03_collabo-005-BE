from django.urls import path

from .views import (
    CustomUserCheckEmailView,
    CustomUserCheckNickView,
    CustomUserLoginView,
    CustomUserSignUpView,
    DeleteUser,
    ResetPassword,
    SendJWTEmail,
    UpdatePassword,
    VerifyJWTEmail,
)

urlpatterns = [
    path("signup/", CustomUserSignUpView.as_view(), name="signup"),
    path("login/", CustomUserLoginView.as_view(), name="login"),
    path("checkEmail/", CustomUserCheckEmailView.as_view(), name="check_email"),
    path("checkNickname/", CustomUserCheckNickView.as_view(), name="check_nick"),
    path("delete/", DeleteUser.as_view(), name="delete_user"),
    # path("cancerDelete/", CancelDeleteuser.as_view(), name="cancer_delete_user"),
    path("send/email/token/", SendJWTEmail.as_view(), name="send_email_token"),
    path("verify/email/", VerifyJWTEmail.as_view(), name="verify_email"),
    path("new/password/", UpdatePassword.as_view(), name="update_password"),
    path("reset/password/", ResetPassword.as_view(), name="reset_password"),
]
