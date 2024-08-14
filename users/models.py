from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from common.models import CommonModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email은 필수 입력 사항입니다.")
        if not password:
            raise ValueError("Password는 필수 입력 사항입니다.")

        # normalize_email 메서드는 사용자가 입력한 이메일 주소를 대소문자를 일치시켜 표준화된 형식으로 변환한다.
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        # super user도 is_staff 기능이 있어야 admin 페이지에 접속 가능하다.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin, CommonModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=50, unique=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    introduction = models.TextField(null=True, blank=True)
    fti_type = models.CharField(max_length=50, null=True)
    taste_type = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    # 이메일을 유저네임 필드로 사용
    USERNAME_FIELD = "email"
    # 슈퍼유저를 생성할 때 반드시 입력받아야 하는 필드
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
