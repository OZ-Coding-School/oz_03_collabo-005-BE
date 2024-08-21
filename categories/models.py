from django.db import models


class ReviewCategory(models.Model):
    category = models.TextField()


class Location(models.Model):
    location_name = models.CharField(max_length=100)


class MeetingPaymentMethod(models.Model):
    payment_method = models.CharField(max_length=100)


class MeetingAgeGroup(models.Model):
    age_group = models.CharField(max_length=100)


class MeetingGenderGroup(models.Model):
    gender_group = models.CharField(max_length=100)


class FTIType(models.Model):
    fti_type = models.CharField(max_length=10)
    description = models.TextField()
