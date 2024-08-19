from django.db import models

from common.models import CommonModel


class FoodTag(models.Model):
    food_tag = models.CharField(max_length=50)


class Food(CommonModel):
    food_name = models.CharField(max_length=50)
    oil_preference = models.PositiveIntegerField(models.SET_NULL, null=True)
    noodle_preference = models.PositiveIntegerField(models.SET_NULL, null=True)
    rice_preference = models.PositiveIntegerField(models.SET_NULL, null=True)
    spicy_preference = models.PositiveIntegerField(models.SET_NULL, null=True)
    instant_preference = models.PositiveIntegerField(models.SET_NULL, null=True)
    price_preference = models.PositiveIntegerField(models.SET_NULL, null=True)
    image_url = models.ImageField()
    food_tag = models.ManyToManyField(FoodTag, related_name="foods")
