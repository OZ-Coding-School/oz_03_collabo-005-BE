import uuid

from django.db import models
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from comments.models import ReviewComment
from common.models import CommonModel
from likes.models import ReviewLike


class Review(CommonModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        "categories.ReviewCategory", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=150)
    content = models.TextField()
    hits = models.PositiveIntegerField(default=0)
    review_image_url = models.URLField(null=True, blank=True)
    is_host = models.BooleanField(default=True)

    @property
    def likes_count(self):
        return ReviewLike.objects.filter(review_id=self.pk).count()

    @property
    @extend_schema_field(serializers.IntegerField)
    def comment_count(self):
        return ReviewComment.objects.filter(review_id=self.pk).count()

    def __str__(self):
        return self.title
