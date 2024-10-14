import random

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from common.models import CommonModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, nickname, **extra_fields):
        if not email:
            raise ValueError("Email은 필수 입력 사항입니다.")
        if not password:
            raise ValueError("Password는 필수 입력 사항입니다.")
        if not nickname:
            raise ValueError("Nickname은 필수 입력 사항입니다.")

        # normalize_email 메서드는 사용자가 입력한 이메일 주소를 대소문자를 일치시켜 표준화된 형식으로 변환한다.
        email = self.normalize_email(email)
        user = self.model(email=email, nickname=nickname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, nickname, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, nickname, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, CommonModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=50, unique=True)
    profile_image_url = models.URLField(max_length=200, null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    fti_type = models.ForeignKey(
        "categories.FTIType", null=True, on_delete=models.CASCADE
    )
    spicy_preference = models.PositiveIntegerField(null=True, default=None)
    intensity_preference = models.PositiveIntegerField(null=True, default=None)
    oily_preference = models.PositiveIntegerField(null=True, default=None)
    flour_rice_preference = models.PositiveIntegerField(null=True, default=None)
    cost_preference = models.PositiveIntegerField(null=True, default=None)
    spicy_weight = models.PositiveIntegerField(null=True, default=None)
    cost_weight = models.PositiveIntegerField(null=True, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    deleted_at = models.DateField(null=True)

    objects = CustomUserManager()

    # 이메일을 username 필드로 사용
    USERNAME_FIELD = "email"
    # 슈퍼유저를 생성할 때 반드시 입력 받아야 하는 필드
    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return self.email


class EmailVerification(CommonModel):
    email = models.EmailField(unique=True)
    verification_code = models.CharField(max_length=6)

    def generate_verification_code(self):
        self.generate_verification_code = str(random.randint(100000, 999999))

        return self.generate_verification_code
