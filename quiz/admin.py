from django.contrib import admin
from django.core.exceptions import ValidationError
from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import Quiz, Question, Answer
from django.forms import ModelForm, inlineformset_factory
from nested_admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline
from django.forms.models import BaseInlineFormSet
from django.forms import forms


class QuestionModelFormSet(BaseInlineFormSet):
    class Meta:
        model = Question
        fields = "__all__"


    def clean(self):
        list_title = []

        for form in self.forms:
            form_clean = form.cleaned_data
            if not form_clean:
                raise forms.ValidationError('Нужно задать вопрос')
            if form_clean['title'] not in list_title:
                list_title.append(form_clean['title'])
            else:
                # form.clean_title({'cast_error': 'sss'})
                raise forms.ValidationError(f'Дубль вопроса {form_clean["title"]}')


class AnswerModelFormSet(BaseInlineFormSet):
    class Meta:
        model = Answer
        fields = "__all__"

    def clean(self):
        it_true_answer_count = 0
        answer_count = 0
        list_title = []
        for form in self.forms:
            form_clean = form.cleaned_data
            if not form_clean.get('title'):
                raise forms.ValidationError('Нужно заполнить все ответы ')
            elif form_clean['title'] not in list_title:
                list_title.append(form_clean['title'])
            else:
                raise forms.ValidationError(f'Дубль ответа {form_clean["title"]}')
            if form_clean.get("is_true") is True:
                it_true_answer_count += 1
            answer_count += 1
        if it_true_answer_count == 0:
            raise forms.ValidationError('Нужен хотя бы одни правильный ответ')
        if it_true_answer_count == answer_count:
            raise forms.ValidationError('Все ответы не могут быть верными')


class QuestionAdminForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 1:
            raise ValidationError('Хоть что нибудь напишите')
        return title


class AnswerAdminForm(ModelForm):
    class Meta:
        model = Answer
        fields = '__all__'

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 1:
            raise ValidationError('Хоть что нибудь напишите')
        return title


class AnswerInline(NestedTabularInline):
    formset = AnswerModelFormSet
    model = Answer
    extra = 1
    fields = ('title', 'is_true',)
    form = AnswerAdminForm


class QuestionInline(NestedStackedInline):
    formset = QuestionModelFormSet
    model = Question
    inlines = [AnswerInline]
    extra = 1
    fields = ('title',)
    form = QuestionAdminForm


class QuizAdminForm(ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 1:
            raise ValidationError('Хоть что нибудь напишите')
        return title


class QuizAdmin(NestedModelAdmin):
    inlines = [QuestionInline]
    form = QuizAdminForm


admin.site.register(Quiz, QuizAdmin)
