# Generated by Django 4.2 on 2024-09-02 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meetings", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="meeting",
            name="time_sort",
        ),
    ]
