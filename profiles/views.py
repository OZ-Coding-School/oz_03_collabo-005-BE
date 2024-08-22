from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser

from .serializers import ProfileSerializer


# 유저의 프로필 조회
class ProfileView(APIView):
    serializer_class = ProfileSerializer

    @extend_schema(tags=["profile"])
    def get(self, request):
        try:
            profile = CustomUser.objects.get(id=request.user.id)
        except CustomUser.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance=profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
