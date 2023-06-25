from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import Profile
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404, reverse
import re

email_val = r'^[a-zA-Z0-9]([A-Za-z0-9]+[._-])*[A-Za-z0-9_]+@[A-Za-z0-9-_]+(\.[A-Z|a-z]{2,})+$'


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control text-center',
                                                                          'placeholder': 'Введите почту'}))

    username = forms.CharField(required=True, max_length=15, label='Введите логин',
                               help_text='Нельзя вводить символы @, /, _.',
                               widget=forms.TextInput(attrs={'class': 'form-control text-center',
                                                             'placeholder': 'Введите логин'}))

    password1 = forms.CharField(required=True, label='Введтие пароль', help_text='Пароль должен быть длинным',
                                widget=forms.PasswordInput(attrs={'class': 'form-control text-center'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        try:
            password_validation.validate_password(password1, self.instance)
        except forms.ValidationError as error:
            self.add_error('password1', error)
        return password1

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(email_val, email):
            raise ValidationError('Проверьте правильность ввода email')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='',
                             widget=forms.TextInput(attrs={'class': 'form-control text-center',
                                                           'placeholder': 'Введите почту'}))

    username = forms.CharField(required=True, label='',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control text-center', 'placeholder': 'Введите логин'}))

    class Meta:
        model = User
        fields = ['email', 'username']


class ProfileImageForm(forms.ModelForm):
    img = forms.ImageField(
        label="",
        required=True,
        widget=forms.FileInput(
            attrs={'class': 'form-control text-center'}),

    )

    class Meta:
        model = Profile
        fields = ['img']


class AuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control text-center', 'placeholder': 'Введите логин'}))
    password = forms.CharField(label='Пароль пользователя',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control text-center', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User


class EmailValidationPasswordResetView(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(email_val, email):
            raise ValidationError('Проверьте правильность ввода email')
        elif not User.objects.filter(email=email).exists():
            raise ValidationError("Пользователя с такой почтой не существует")
        return email
