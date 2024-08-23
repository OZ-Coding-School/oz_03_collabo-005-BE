from django.db import models

from common.models import CommonModel


class Meeting(CommonModel):
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
    image_url = models.ImageField()
    hits = models.PositiveIntegerField(default=0)

    @property
    def likes_count(self):
        return self.meeting_like.count()


class MeetingMember(CommonModel):
    meeting = models.ForeignKey(
        "meetings.Meeting", on_delete=models.CASCADE, related_name="meeting_id"
    )
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)
    is_host = models.BooleanField(default=False)

    class Meta:
        unique_together = ("meeting", "user")
