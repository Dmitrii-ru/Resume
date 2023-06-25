from django.db import models


class Todo(models.Model):

    CHOICES = (
        (1, 'Высокий приоритет'),
        (2, 'Средний приоритет'),
        (3, 'Низкий приоритет'),
    )

    title = models.CharField('Название', max_length=20)
    priority = models.CharField('Приоритет', max_length=15, choices=CHOICES)
    text = models.TextField('Суть задачи', max_length=1000)
