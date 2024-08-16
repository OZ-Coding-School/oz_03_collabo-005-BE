from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import SignUpUserSerializer
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse


# 회원가입
class CustomUserSignUpView(APIView):
    serializer_class = SignUpUserSerializer
    @extend_schema(tags=["User"],
        operation_id='CustomUserSignUp',
        summary=" 회원가입",
        examples=[
            OpenApiExample(
                name="Example",
                value={'email': "abc@abc.com", "password":"pass123"},
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


#  로그인
class CustomUserLoginView(APIView):
    serializer_class = SignUpUserSerializer
    @extend_schema(tags=["User"],
        operation_id='CustomUserLogin',
        summary=" 로그인",
        examples=[
            OpenApiExample(
                name="Example",
                value={'email': "abc@abc.com", "password":"pass123"},
                request_only=True,
            )
        ],
        description="JWT Login",
       responses={
           200:OpenApiResponse(
               description="로그인성공"
           ),
           400: OpenApiResponse(
               description="로그인실패"
           ),
       }
    )
    def post(self, request):
        pass


#post 방식으로 개인정보 수신

#DB에서 해당 정보가 일치하는지 확인

#Access, Refresh Token 발행







