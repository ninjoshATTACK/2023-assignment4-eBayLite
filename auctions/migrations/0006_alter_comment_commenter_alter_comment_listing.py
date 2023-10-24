# Generated by Django 4.1.2 on 2023-10-24 03:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_comment_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='commenter',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='listing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listing'),
        ),
    ]
