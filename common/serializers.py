from rest_framework import serializers

from test_info.models import FTITestQuestion, TasteTestQuestion, TasteTestAnswer


class FTITestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FTITestQuestion
        fields = ("fti_question",)


class UserFTITestResultSerializer(serializers.Serializer):
    fti_style = serializers.ListField(
        child=serializers.CharField(max_length=3),
    )


# TasetTestQuestion
class BulkCreateTasteTestQuestion(serializers.ModelSerializer):
    class Meta:
        model = TasteTestQuestion
        fields = "__all__"


# TasetTestAnswer
class BulkCreateTasteTestAnswer(serializers.ModelSerializer):
    class Meta:
        model = TasteTestAnswer
        fields = "__all__"
