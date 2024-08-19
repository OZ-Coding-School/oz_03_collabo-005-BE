from django.db import models

from common.models import CommonModel


class FoodTag(models.Model):
    food_tag = models.CharField(max_length=50)


class Food(CommonModel):
    food_name = models.CharField(max_length=50)
    oil_preference = models.PositiveIntegerField(default=None, null=True)
    noodle_preference = models.PositiveIntegerField(default=None, null=True)
    rice_preference = models.PositiveIntegerField(default=None, null=True)
    spicy_preference = models.PositiveIntegerField(default=None, null=True)
    instant_preference = models.PositiveIntegerField(default=None, null=True)
    price_preference = models.PositiveIntegerField(default=None, null=True)
    image_url = models.ImageField()
    food_tag = models.ManyToManyField(FoodTag, related_name="foods")
