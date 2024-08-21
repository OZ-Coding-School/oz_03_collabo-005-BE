from django.db import models

from common.models import CommonModel


class Food(CommonModel):
    food_name = models.CharField(max_length=50)
    spicy_preference = models.PositiveIntegerField(default=None, null=True)
    intensity_preference = models.PositiveIntegerField(default=None, null=True)
    oily_preference = models.PositiveIntegerField(default=None, null=True)
    flour_rice_preference = models.PositiveIntegerField(default=None, null=True)
    cost_preference = models.PositiveIntegerField(default=None, null=True)
    spicy_weight = models.PositiveIntegerField(default=None, null=True)
    cost_weight = models.PositiveIntegerField(default=None, null=True)
    is_launch = models.BooleanField()
    is_dinner = models.BooleanField()
    is_snack = models.BooleanField()
    is_date = models.BooleanField()
    is_party = models.BooleanField()
    is_diet = models.BooleanField()
    image_url = models.ImageField()
