import random

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.exceptions import (
    NotFound,
    ParseError,
    PermissionDenied,
    ValidationError,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, EmailVerification
from .serializers import (
    DetailUserSerializer,
    LoginUserSerializer,
    SendEmailTokenSerializer,
    SignUpUserSerializer,
    UpdatePasswordSerializer,
    VerifyEmailSerializer,
)


# 회원가입
class CustomUserSignUpView(APIView):
    serializer_class = SignUpUserSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["User"],
        operation_id="CustomUserSignUp",
        summary=" 회원가입",
        examples=[
            OpenApiExample(
                name="Example",
                value={
                    "email": "abcabc@abcabc.com",
                    "password": "pass123!",
                    "nickname": "중복불가1",
                },
                request_only=True,
            )
        ],
        description="JWT Login",
    )
    def post(self, request):
        data = request.data

        # 이메일 중복 체크
        if CustomUser.objects.filter(email=data.get("email")).exists():
            return Response(
                {"error": "이미 사용 중인 이메일입니다"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 닉네임 중복 체크
        if CustomUser.objects.filter(nickname=data.get("nickname")).exists():
            return Response(
                {"error": "이미 사용 중인 닉네임입니다"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SignUpUserSerializer(data=data)
        if serializer.is_valid():
            user = CustomUser(
                email=serializer.validated_data["email"],
                nickname=serializer.validated_data["nickname"],
            )
            user.set_password(serializer.validated_data["password"])
            user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class CustomUserLoginView(APIView):
    serializer_class = SignUpUserSerializer
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["User"],
        operation_id="CustomUserLogin",
        summary=" 로그인",
        examples=[
            OpenApiExample(
                name="Example",
                value={"email": "abcabc@abcabc.com", "password": "pass123!"},
                request_only=True,
            )
        ],
        description="JWT Login",
        responses={
            200: OpenApiResponse(description="로그인성공"),
            400: OpenApiResponse(description="로그인실패"),
        },
    )
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)

        # post 방식으로 개인정보 수신
        # DB에서 해당 정보가 일치하는지 확인
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    # Access, Refresh Token 발행
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(serializer.errors, status=400)


# 중복확인 이메일
class CustomUserCheckEmailView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["User"],
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample(
                name="Email Check",
                value={"email": "bobpience@babpiens.com"},
                description="이메일 중복체크",
            )
        ],
        responses={200: OpenApiResponse(description="Success")},
    )
    def post(self, request):
        email = request.data.get("email")

        # 이메일 중복 체크
        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {"error": "이미 사용 중인 이메일입니다"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=200)


# 중복확인 닉네임
class CustomUserCheckNickView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["User"],
        request=OpenApiTypes.OBJECT,
        examples=[
            OpenApiExample(
                name="Nickname Check",
                value={"nickname": "중복불가1"},
                description="닉네임 중복 체크",
            )
        ],
        responses={200: OpenApiResponse(description="Success")},
    )
    def post(self, request):
        nickname = request.data.get("nickname")

        # 이메일 중복 체크
        if CustomUser.objects.filter(nickname=nickname).exists():
            return Response(
                {"error": "이미 사용 중인 닉네임입니다"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=200)


# 회원 탈퇴
class DeleteUser(APIView):
    serializer_class = LoginUserSerializer

    @extend_schema(tags=["User"])
    def post(self, request):
        user = request.user
        try:
            password = request.data["password"]
        except KeyError:
            raise ParseError("Need Password")

        if not user.check_password(password):
            raise ParseError("Password is not valid")

        user.deleted_at = timezone.localtime(timezone.now()).date()
        user.is_active = False
        user.save()

        serializer = DetailUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


# 이메일 인증번호 전송
class SendVerificationCode(APIView):

    permission_classes = (AllowAny,)
    serializer_class = SendEmailTokenSerializer

    @extend_schema(tags=["User"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            email = request.data["email"]

        except KeyError:
            raise ParseError("Need email")

        verification_code = EmailVerification.generate_verification_code
        EmailVerification.objects.create(
            email=email, verification_code=verification_code
        )
        subject = "이메일 인증 코드"
        message = f"이메일 인증을 위해 아래 인증 번호를 입력해 주세요. \n\n{verification_code}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        return Response(status=status.HTTP_200_OK)


# 이메일 인증번호 검증
class VerifyEmail(APIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifyEmailSerializer

    @extend_schema(tags=["User"])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            email = request.data["email"]
            request_code = request.data["code"]
            send_code = EmailVerification.objects.get(email=email).verification_code

        except KeyError:
            raise ParseError

        except EmailVerification.DoesNotExist:
            raise NotFound

        if request_code != send_code:
            raise ValidationError

        EmailVerification.objects.get(email=email).delete()

        return Response(status=status.HTTP_200_OK)


# 회원 탈퇴 취소
# class CancelDeleteuser(APIView):
#
#     serializer_class = LoginUserSerializer
#     @extend_schema(tags=["User"])
#     def post(self, request):
#         user = request.user
#         try:
#             password = request.data["password"]
#         except KeyError:
#             raise ParseError("Need Password")
#
#         if not user.check_password(password):
#             raise ParseError("Password is not valid")
#
#         user.is_active = True
#         user.deleted_at = None
#         user.save()
#
#         serializer = DetailUserSerializer(user)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)


# 비밀번호 재설정
class UpdatePassword(APIView):

    serializer_class = UpdatePasswordSerializer

    @extend_schema(tags=["User"])
    def post(self, request):
        user = request.user

        try:
            old_password = request.data["old_password"]
            new_password = request.data["new_password"]
        except KeyError:
            raise ParseError

        if not user.check_password(old_password):
            raise ValidationError("Mistake in the password")

        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_200_OK)


class ResetPassword(APIView):

    permission_classes = (AllowAny,)
    serializer_class = UpdatePasswordSerializer(partial=True)

    @extend_schema(tags=["User"])
    def post(self, request):
        try:
            email = request.data["email"]
            request_code = request.data["code"]
            send_code = EmailVerification.objects.get(email=email).verification_code
            new_password = str(random.randint(100000, 999999))

        except KeyError:
            raise ParseError

        except EmailVerification.DoesNotExist:
            raise NotFound

        if request_code != send_code:
            raise ValidationError

        subject = "이메일 인증 코드"
        message = f"새로운 비밀번호입니다. 보안을 위해 비밀번호를 변경해주세요. \n\n{new_password}"

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

        return Response(status=status.HTTP_200_OK)
