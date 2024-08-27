import uuid

from django.db import models

from common.models import CommonModel
from likes.models import ReviewLike
from comments.models import ReviewComment


class Review(CommonModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        "categories.ReviewCategory", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=150)
    content = models.TextField()
    hits = models.PositiveIntegerField()
    review_image_url = models.URLField(null=True, blank=True)
    is_host = models.BooleanField(null=True)

    @property
    def likes_count(self):
        return ReviewLike.objects.filter(review_id=self.pk).count()

    @property
    def comment_count(self):
        return ReviewComment.objects.filter(review_id=self.pk).count()

    def __str__(self):
        return self.title
