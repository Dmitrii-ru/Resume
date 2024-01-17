from django import forms
from django.forms import formset_factory, inlineformset_factory
from .models import Quiz, Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title']


AnswerFormSet = formset_factory(forms.ModelForm, formset=forms.BaseFormSet, min_num=2, validate_min=True, extra=2,
                                can_delete=True)


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']


QuizFormSet = formset_factory(QuizForm, extra=1)
