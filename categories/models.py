from django.db import models


class ReviewCategory(models.Model):
    category = models.CharField()

    def __str__(self):
        return self.category


class Location(models.Model):
    location_name = models.CharField(max_length=100)

    def __str__(self):
        return self.location_name


class TimeSortCategory(models.Model):
    sort_name = models.CharField(max_length=20)

    def __str__(self):
        return self.sort_name


class MeetingPaymentMethod(models.Model):
    payment_method = models.CharField(max_length=100)

    def __str__(self):
        return self.payment_method


class MeetingAgeGroup(models.Model):
    age_group = models.CharField(max_length=100)

    def __str__(self):
        return self.age_group


class MeetingGenderGroup(models.Model):
    gender_group = models.CharField(max_length=100)

    def __str__(self):
        return self.gender_group


class FTIType(models.Model):
    fti_type = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.fti_type


class FoodFilter(models.Model):
    filter_name = models.CharField(max_length=20)
    filter_value = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.filter_name}: {self.filter_value}"
