from rest_framework import serializers

from .models import CustomUser


class SignUpUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "nickname", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
