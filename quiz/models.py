from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Quiz(models.Model):
    title = models.CharField('Тема опроса', max_length=30, blank=False, unique=True)
    is_completed = models.ManyToManyField(User, related_name='quiz_completed', blank=True,verbose_name='Прошли тест')

    def __str__(self):
        return self.title

    def get_absolute_url(self, **kwargs):
        return reverse('quiz_urls:index_quiz')

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class Question(models.Model):
    parent_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField('Вопрос', max_length=200, blank=False)
    is_completed = models.ManyToManyField(User, related_name='completed', default=None, blank=True)
    is_right_user_completed = models.ManyToManyField(User, related_name='right_completed', default=None, blank=True)

    def __str__(self):
        return f'{self.parent_quiz} - {self.title}'

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы "

class Answer(models.Model):
    parent_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    title = models.CharField('Ответ', max_length=200, blank=False)
    is_true = models.BooleanField(default=False)
    is_user_answer = models.ManyToManyField(User, related_name='user_answer', default=None, blank=True)

    def __str__(self):
        return f'{self.parent_question} - {self.title}'

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"