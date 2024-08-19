from django.db import models

from common.models import CommonModel


class Review(CommonModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        "categories.ReviewCategory", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=150)
    content = models.TextField()
