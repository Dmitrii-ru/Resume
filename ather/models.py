import datetime
from datetime import timezone
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.db import models
from pytils.translit import slugify


def time_time_now(date):
    return timezone.localtime(date).strftime("%Y-%m-%d %H:%M:%S")


class Person(models.Model):
    name = models.CharField('Персона', max_length=40, blank=False)
    slug = models.SlugField('slug', default='', blank=False)
    visit_password = models.CharField('Пароль для просмотра', max_length=10, blank=False)
    text1 = RichTextField('Текс1', blank=True)
    text2 = RichTextField('Текс2', blank=True)
    video_link = models.URLField('Ссылка на видео', blank=True)
    image = models.ImageField(
        upload_to='image',
        blank=True,

    )
    is_active = models.BooleanField('Опубликовано ', default=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} Создан: {time_time_now(self.date)} '

    def save(self, *args, **kwargs):
        self.slug = f'{self.slug}date{time_time_now(self.date)}'
        super().save(*args, **kwargs)


class ImagesProductsShop(models.Model):
    person = models.ForeignKey(
        Person,
        default='image_default/default.png',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='image',
        blank=True
    )

    class Meta:
        verbose_name = 'Фото галерея'
        verbose_name_plural = 'Фото галерея'
