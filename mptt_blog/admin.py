from django.contrib.auth.models import User
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Post, Category
from .forms import CategoryFormAdmin, PostFormAdmin, PostValidationMixin
from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget


class PostAdmin(admin.ModelAdmin):
    author = forms.CharField(label='Автор')
    form = PostFormAdmin


admin.site.register(Post, PostAdmin)


class CategoryAdmin(DjangoMpttAdmin):
    form = CategoryFormAdmin
    readonly_fields = [
        'url',
    ]


admin.site.register(Category, CategoryAdmin)
