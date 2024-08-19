from django.db import models

from common.models import CommonModel


class ReviewComment(CommonModel):
    review = models.ForeignKey("reviews.Review", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)
    content = models.TextField()


class MeetingComment(CommonModel):
    meeting = models.ForeignKey("meetings.Meeting", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)
    content = models.TextField()
