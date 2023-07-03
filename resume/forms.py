from django import forms
from .models import EmailSend
from django.core.exceptions import ValidationError
from validate_email import validate_email
from django.contrib.sessions.backends.db import SessionStore
import re
from user_app.user_session import UserSessionToDo
from .models import CardProject

reg = r'^[a-zA-Z0-9]([A-Za-z0-9]+[._-])*[A-Za-z0-9_]+@[A-Za-z0-9-_]+(\.[A-Z|a-z]{2,})+$'


class EmailSendForm(forms.ModelForm):
    class Meta:
        model = EmailSend
        fields = ('name', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(reg, email):
            raise ValidationError('Проверьте правильность ввода email')
        return email

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2 or any(map(str.isdigit, name)):
            raise ValidationError('Где вы видели такой имя')
        return name.title()


class AddTodo(forms.Form):
    todo = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Новая задача'}), label='', required=False,
                           max_length=20)
    day_slug = forms.CharField(widget=forms.HiddenInput)
    sess = forms.CharField(widget=forms.HiddenInput)

    def clean(self):

        ust = UserSessionToDo(SessionStore(self.cleaned_data['sess']), sess=True)
        day = ust.todo_days[self.cleaned_data['day_slug']]
        todo = self.cleaned_data['todo']
        if not todo:
            raise ValidationError(
                f"Вы нечего не ввели")
        elif len(todo) > 20:
            raise ValidationError(
                "Не больше 35 символов")
        elif todo in day['actual']:
            raise ValidationError(
                f"Уже есть в Задачах на сегодня")
        elif todo in day['close']:
            raise ValidationError(
                f"Уже есть в Завершенных задачах")
        return todo


class TestForm(forms.ModelForm):
    model = CardProject
