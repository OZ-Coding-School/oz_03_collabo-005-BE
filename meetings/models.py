import uuid

from django.db import models
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from common.models import CommonModel
from likes.models import MeetingLike


class Meeting(CommonModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    location = models.ForeignKey(
        "categories.Location", on_delete=models.SET_NULL, null=True
    )
    payment_method = models.ForeignKey(
        "categories.MeetingPaymentMethod", on_delete=models.SET_NULL, null=True
    )
    age_group = models.ForeignKey(
        "categories.MeetingAgeGroup", on_delete=models.SET_NULL, null=True
    )
    gender_group = models.ForeignKey(
        "categories.MeetingGenderGroup", on_delete=models.SET_NULL, null=True
    )
    meeting_time = models.DateTimeField()
    description = models.TextField()
    meeting_image_url = models.URLField(null=True)
    hits = models.PositiveIntegerField(default=0)
    maximum = models.PositiveIntegerField()

    @property
    @extend_schema_field(serializers.IntegerField)
    def likes_count(self):
        return MeetingLike.objects.filter(meeting_id=self.pk).count()

    def __str__(self):
        return self.title


class MeetingMember(CommonModel):
    meeting = models.ForeignKey(
        "meetings.Meeting", on_delete=models.CASCADE, related_name="meeting"
    )
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)
    is_host = models.BooleanField(default=False)

    class Meta:
        unique_together = ("meeting", "user")

    def __str__(self):
        return f"{self.meeting},{self.user}"
