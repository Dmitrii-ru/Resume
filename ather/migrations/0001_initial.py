# Generated by Django 4.2 on 2023-08-30 10:46

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, verbose_name='Персона')),
                ('visit_password', models.CharField(blank=True, max_length=10, verbose_name='Пароль для просмотра')),
                ('text1', ckeditor.fields.RichTextField(verbose_name='Текс1')),
                ('text2', ckeditor.fields.RichTextField(verbose_name='Текс2')),
                ('video_link', models.URLField(verbose_name='Ссылка на видео')),
                ('image', models.ImageField(blank=True, upload_to='image')),
                ('is_active', models.BooleanField(default=True, verbose_name='Опубликовано ')),
            ],
        ),
        migrations.CreateModel(
            name='ImagesProductsShop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='image')),
                ('person', models.ForeignKey(default='image_default/default.png', on_delete=django.db.models.deletion.CASCADE, to='ather.person')),
            ],
            options={
                'verbose_name': 'Фото галерея',
                'verbose_name_plural': 'Фото галерея',
            },
        ),
    ]
