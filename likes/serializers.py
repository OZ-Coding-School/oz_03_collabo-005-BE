from rest_framework import serializers


class LikeSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
