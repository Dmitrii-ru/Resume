# Generated by Django 4.2 on 2023-08-30 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ather', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='slug',
            field=models.SlugField(default='', verbose_name='slug'),
        ),
    ]
