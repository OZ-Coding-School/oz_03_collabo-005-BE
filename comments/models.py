from django.db import models

from common.models import CommonModel


class ReviewComment(CommonModel):
    review = models.ForeignKey("reviews.Review", on_delete=models.CASCADE, related_name="review_comments")
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.review}, {self.content}"


class MeetingComment(CommonModel):
    meeting = models.ForeignKey("meetings.Meeting", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)
    content = models.TextField()
