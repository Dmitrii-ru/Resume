# Generated by Django 4.2 on 2023-06-08 14:27

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='style_btn1',
        ),
        migrations.AlterField(
            model_name='aboutme',
            name='text',
            field=ckeditor.fields.RichTextField(max_length=2000, verbose_name='О себе'),
        ),
        migrations.AlterField(
            model_name='cardproject',
            name='text',
            field=ckeditor.fields.RichTextField(max_length=10000, verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='cardproject',
            name='title',
            field=models.CharField(max_length=40, verbose_name='Тема'),
        ),
        migrations.DeleteModel(
            name='Style',
        ),
    ]
