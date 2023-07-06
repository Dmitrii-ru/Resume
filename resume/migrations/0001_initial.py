# Generated by Django 4.2 on 2023-07-05 23:03

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AboutMe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField(max_length=2000, verbose_name='О себе')),
                ('phone', models.CharField(max_length=30, verbose_name='Телефон')),
                ('city', models.CharField(max_length=30, verbose_name='Город')),
                ('mail', models.CharField(max_length=30, verbose_name='Почта')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('education_my', models.CharField(max_length=500, verbose_name='Образование не в IT')),
                ('link_HH', models.CharField(blank=True, max_length=100, null=True, verbose_name='HH')),
            ],
            options={
                'verbose_name': 'О себе',
                'verbose_name_plural': 'О себе',
            },
        ),
        migrations.CreateModel(
            name='EmailSend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50, verbose_name='Почта')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MyEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название курса')),
                ('school', models.CharField(max_length=200, verbose_name='Школа')),
                ('end', models.CharField(blank=True, max_length=20, null=True, verbose_name='Дата окончания')),
                ('diploma', models.CharField(blank=True, max_length=200, null=True, verbose_name='Ссылка на диплом')),
                ('percent', models.IntegerField(verbose_name='Процент завершения курса')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Образование',
            },
        ),
        migrations.CreateModel(
            name='Stack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название технологии')),
                ('slug', models.SlugField(verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Стэк',
                'verbose_name_plural': 'Стэки',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(verbose_name='Слаг')),
                ('name', models.CharField(max_length=50, verbose_name='Название проекта')),
                ('about', models.CharField(max_length=200, verbose_name='О проекте')),
                ('image', models.ImageField(blank=True, default='default_project.png', null=True, upload_to='img', verbose_name='Ава проекта')),
                ('status', models.CharField(choices=[('True', 'Завершен'), ('False', 'В работе')], default='True', max_length=5, verbose_name='Статус')),
                ('link_git', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ссылка на GitHub')),
                ('link_site', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ссылка на WebSite')),
                ('stacks', models.ManyToManyField(related_name='project_stacks', to='resume.stack', verbose_name='Технологии проекта')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='CardProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40, verbose_name='Тема')),
                ('text', ckeditor.fields.RichTextField(max_length=10000, verbose_name='Текст')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Карточка',
                'verbose_name_plural': 'Карточки',
            },
        ),
    ]
