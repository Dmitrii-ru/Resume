# Generated by Django 4.2 on 2023-07-30 23:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0005_uniqueip_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uniqueip',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]