from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from pytils.translit import slugify
from ckeditor.fields import RichTextField

CHOICE_STATUS = [
    ('True', 'Завершен'),
    ('False', 'В работе')
]


class MyEducation(models.Model):
    name = models.CharField('Название курса', max_length=200)
    school = models.CharField('Школа', max_length=200)
    end = models.CharField('Дата окончания', max_length=20, null=True, blank=True)
    diploma = models.CharField('Ссылка не диплом', max_length=200, null=True, blank=True)
    percent = models.IntegerField('Процент завершения курса')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Образование"


class AboutMe(models.Model):
    text = RichTextField('О себе', max_length=2000)
    phone = models.CharField('Телефон', max_length=30)
    city = models.CharField('Город', max_length=30)
    mail = models.CharField('Почта', max_length=30)
    name = models.CharField('Имя', max_length=50)
    education_my = models.CharField('Образование не в IT', max_length=500)
    link_HH = models.CharField('HH', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "О себе"
        verbose_name_plural = "О себе"


class Stack(models.Model):
    name = models.CharField('Название технологии', max_length=20)
    slug = models.SlugField('Слаг', null=False, db_index=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        print(self)
        return reverse('resume_urls:stack', kwargs={'stack_slug': self.slug})

    class Meta:
        verbose_name = "Стэк"
        verbose_name_plural = "Стэки"


class Projects(models.Model):
    slug = models.SlugField('Слаг', null=False, db_index=True)
    prod_stack = models.ManyToManyField(Stack, verbose_name='Технологии проекта', related_name='ps')
    name = models.CharField('Название проекта', max_length=50)
    about = models.CharField('О проекте', max_length=200)
    image = models.ImageField('Ава проекта', upload_to='img', null=True, blank=True, default='default_project.png')
    status = models.CharField('Статус', choices=CHOICE_STATUS, default="True", max_length=5)
    link_git = models.CharField('Ссылка на GitHub', max_length=100, null=True, blank=True)
    link_site = models.CharField('Ссылка на WebSite', max_length=100, null=True, blank=True)
    style_btn2 = models.CharField('Цвет обводки', max_length=100, null=True, blank=True, default='black')

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Projects, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class EmailSend(models.Model):
    email = models.CharField('Почта', max_length=50)
    name = models.CharField('Имя', max_length=50)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.email} - {self.date}'


class CardProject(models.Model):
    project = models.ForeignKey(Projects, verbose_name='Проект', on_delete=models.CASCADE)
    title = models.CharField('Тема', max_length=40)
    text = RichTextField('Текст', max_length=10000)

    def __str__(self):
        return f'{self.project} - {self.title}'

    class Meta:
        verbose_name = "Карточка"
        verbose_name_plural = "Карточки"





