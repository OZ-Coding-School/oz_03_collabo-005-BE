# Generated by Django 4.2 on 2024-10-10 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0004_rename_relation_ftitype_bad_relation_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="ftitype",
            name="bad_reason",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="ftitype",
            name="good_reason",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
