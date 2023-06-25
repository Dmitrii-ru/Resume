# Generated by Django 4.2 on 2023-04-19 18:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mptt_blog', '0004_alter_post_favourites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='favourites',
            field=models.ManyToManyField(blank=True, default=None, related_name='favourite_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
