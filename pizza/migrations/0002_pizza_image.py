# Generated by Django 4.2.7 on 2023-11-24 18:04

from django.db import migrations, models
import helpers.media_upload


class Migration(migrations.Migration):
    dependencies = [
        ("pizza", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pizza",
            name="image",
            field=models.ImageField(
                blank=True, upload_to=helpers.media_upload.upload_pizza_image
            ),
        ),
    ]
