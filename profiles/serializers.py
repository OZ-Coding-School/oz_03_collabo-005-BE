from rest_framework import serializers

from users.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "nickname",
            "profile_image",
            "introduction",
            "fti_type",
        )
