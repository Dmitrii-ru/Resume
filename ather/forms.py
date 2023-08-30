from django import forms


class VisitCongratulation(forms.Form):
    visit_password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Введите пароль'
            }
        ), label='', max_length=10
    )


