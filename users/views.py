from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import LoginUserSerializer, SignUpUserSerializer


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
        parameters=[
            OpenApiParameter(
                name='email',
                description='확인할 이메일을 입력해주세요.',
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        name='Example 1',
                        value='bobpience@babpiens.com',
                        description='An example string value for param1'
                    )
                ]
            )
        ],
        responses={200: OpenApiResponse(description="Success")},
    )
    def get(self, request):
        email = request.query_params.get("email")

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
        parameters=[
            OpenApiParameter(
                name='nickname',
                description='확인할 닉네임을 입력해주세요.',
                required=True,
                type=OpenApiTypes.STR,
                examples=[
                    OpenApiExample(
                        name='Example 1',
                        value='bobdori',
                        description='An example string value for param1'
                    )
                ]
            )
        ],
        responses={200: OpenApiResponse(description="Success")},
    )
    def get(self, request):
        nickname = request.query_params.get("nickname")

        # 이메일 중복 체크
        if CustomUser.objects.filter(nickname=nickname).exists():
            return Response(
                {"error": "이미 사용 중인 닉네임입니다"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=200)