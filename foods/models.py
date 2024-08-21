from django.db import models

from common.models import CommonModel


class FoodTag(models.Model):
    food_tag = models.CharField(max_length=50)


class Food(CommonModel):
    food_name = models.CharField(max_length=50)
    spicy_preference = models.PositiveIntegerField()
    intensity_preference = models.PositiveIntegerField()
    oily_preference = models.PositiveIntegerField()
    flour_rice_preference = models.PositiveIntegerField()
    cost_preference = models.PositiveIntegerField()
    spicy_weight = models.PositiveIntegerField()
    cost_weight = models.PositiveIntegerField()
    image_url = models.ImageField()
    is_launch = models.BooleanField()
    is_dinner = models.BooleanField()
    is_snack = models.BooleanField()
    is_date = models.BooleanField()
    is_party = models.BooleanField()
    is_diet = models.BooleanField()
