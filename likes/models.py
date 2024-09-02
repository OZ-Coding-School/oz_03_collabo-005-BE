from django.db import models
from django.db.models import UniqueConstraint

from common.models import CommonModel


class ReviewLike(CommonModel):
    review = models.ForeignKey(
        "reviews.Review", on_delete=models.CASCADE, related_name="review_like"
    )
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["review", "user"], name="unique_review_user_like")
        ]

    def __str__(self):
        return self.review.title


class MeetingLike(CommonModel):
    meeting = models.ForeignKey(
        "meetings.Meeting", on_delete=models.CASCADE, related_name="meeting_like"
    )
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["meeting", "user"], name="unique_meeting_user_like")
        ]

    def __str__(self):
        return self.meeting.title
