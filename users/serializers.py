from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser


# 회원가입
class SignUpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "nickname",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }


# 투두 로그인
class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # 사용자 입력데이터
        email = data.get("email")
        pwd = data.get("password")
        # 사용자 데이터 검증
        if email and pwd:
            user = authenticate(username=email, password=pwd)
            if user:
                data["user"] = user
            else:
                raise serializers.ValidationError("로그인 정보가 올바르지 않습니다.")
        return data
