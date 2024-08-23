from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser

from .serializers import ProfileSerializer, MeetingHistorySerializer


# 유저의 프로필 조회
class ProfileView(APIView):
    serializer_class = ProfileSerializer

    @extend_schema(tags=["profile"])
    def get(self, request):
        try:
            profile = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(instance=profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(tags=["profile"])
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(instance=user, data=request.data)

        # 데이터 유효성
        serializer.is_valid(raise_exception=True)
        updated_nickname = serializer.validated_data.get("nickname")
        updated_profile_image = serializer.validated_data.get("profile_image")
        updated_introduction = serializer.validated_data.get("introduction")

        # 닉네임 중복 확인
        if (
            CustomUser.objects.filter(nickname=updated_nickname)
            .exclude(id=user.id)
            .exists()
        ):
            return Response(
                {"detail": "Nickname already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


# class MeetingHistory(APIView):
#     serializer_class = MeetingHistorySerializer
#
#     @extend_schema(tags=["profile"])
#     def get(self, request):
#         user = request.user
#
#
#         serializer = self.serializer_class(instance=)


