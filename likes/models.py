from django.db import models

from common.models import CommonModel


class ReviewLike(CommonModel):
    review = models.ForeignKey(
        "reviews.Review", on_delete=models.CASCADE, related_name="review_like"
    )
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)


class MeetingLike(CommonModel):
    meeting = models.ForeignKey(
        "meetings.Meeting", on_delete=models.CASCADE, related_name="meeting_like"
    )
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)
