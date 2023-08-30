from django import forms
from django.core.exceptions import ValidationError


class VisitCongratulation(forms.Form):
    visit_password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Введите пароль', 'class': 'form-control text-center'
            }
        ), label='', max_length=10
    )
    password = forms.CharField(widget=forms.HiddenInput)

    def clean(self):
        data = self.cleaned_data
        visit_password = self.cleaned_data['visit_password']
        password = self.cleaned_data['password']
        if visit_password != password:
            raise ValidationError("Не верный пароль")
        return data
