# Generated by Django 4.1.2 on 2023-10-18 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='photo_url',
            field=models.URLField(blank=True),
        ),
    ]
