from django import forms
from .models import Post, Category, CommentsPost
from django.core.exceptions import ValidationError
from ckeditor.widgets import CKEditorWidget

"""Category"""


class CategoryValidationMixin:
    list_title = None

    def clean(self):
        parent = self.cleaned_data.get('parent')
        title = self.cleaned_data.get('title')

        if not title or len(title) < 3:
            raise ValidationError(f"Короткое название темы")
        elif len(title) > 50:
            raise ValidationError(f"Не больше 50 символов")

        if parent:
            list_title = list(parent.get_children().values_list('title', flat=True))
        else:
            list_title = list(Category.objects.filter(level=0).values_list('title', flat=True))

        if self.instance.pk:
            list_title.remove(self.instance.title)

        list_title = list(map(str.lower, list_title))
        if title.lower() in list_title:
            raise ValidationError(f'Уже есть такая тема')


class CategoryCreateForm(CategoryValidationMixin, forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Новая тема'}), label='', required=False,
                            max_length=50)

    class Meta:
        model = Category
        fields = ['title', 'parent']
        widgets = {'parent': forms.HiddenInput()}


class CategoryFormAdmin(CategoryValidationMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryUpdateForm(CategoryValidationMixin, forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите название'}), label='', required=False,
                            max_length=50)

    class Meta:
        model = Category
        fields = ['title', 'parent']
        widgets = {'parent': forms.HiddenInput()}


"""Post"""


class PostValidationMixin:
    list_title = None

    def clean(self):
        title = self.cleaned_data.get('title')
        category = self.cleaned_data.get('category')

        if not title or len(title) < 1:
            raise ValidationError('Длинна названия не меньше 1 символов')

        list_title = list(Post.objects.filter(category=category).values_list('title', flat=True))

        if self.instance.pk:
            list_title.remove(self.instance.title)
        list_title = list(map(str.lower, list_title))

        if title in list_title:
            raise ValidationError(f'Уже есть такая статья')

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise ValidationError(f'Выберете категорию')
        return category

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or len(content) < 1:
            raise ValidationError('Такая коронная статья нам не нужна ')
        elif len(content) > 10000:
            raise ValidationError('Очень длинная статья, не кто не дочитает до конца ')
        return content


class PostFormAdmin(PostValidationMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'





class PostCreateForm(PostValidationMixin, forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Новая статья'}), label='', required=False,
                            max_length=90)
    content = forms.CharField(widget=CKEditorWidget(attrs={'placeholder': 'Содержание'}), label='', required=False,
                              max_length=10000)

    class Meta:
        model = Post
        fields = ['title', 'content', 'is_privat', 'category']
        widgets = {'category': forms.HiddenInput()}


class PostUpdateForm(PostValidationMixin, forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Новая статья'}), label='', required=False,
                            max_length=90)
    content = forms.CharField(widget=CKEditorWidget(attrs={'placeholder': 'Содержание'}), label='', required=False,
                              max_length=10000)

    # content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Содержание'}), label='', required=False,
    #                           max_length=10000)

    class Meta:
        model = Post
        fields = ['title', 'content', 'is_privat', 'category']
        widgets = {'category': forms.HiddenInput()}


class CommentsPostForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Вы можете оставить комментарий ', 'row': '5', 'cols': '5'}),
        label='',
        required=False,
        min_length=1,
        max_length=2000
    )

    class Meta:
        model = CommentsPost
        fields = ['text', 'post']
        widgets = {'post': forms.HiddenInput()}

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 1:
            raise ValidationError(f'Минимум 1 символ')
        return text
