# Generated by Django 5.1.7 on 2025-03-20 16:27

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0003_listing_category_alter_listing_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='traderequest',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='image'),
        ),
    ]
