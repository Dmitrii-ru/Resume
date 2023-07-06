from django.contrib import admin
from .forms import TestForm
from mptt_blog import forms
from .models import *

admin.site.register(MyEducation)
admin.site.register(AboutMe)
admin.site.register(EmailSend)


@admin.register(Stack)
class AdminSteck(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CardProjectInline(admin.StackedInline):
    model = CardProject
    extra = 3
    form = TestForm


class AdminProject(admin.ModelAdmin):
    filter_horizontal = ['stacks']
    fieldsets = (
        ('О проекте', {
            'fields': ('name', 'about', 'image', 'status', 'slug')
        }),
        ('Технологии', {
            'fields': ('stacks',)
        }),
        ('Ссылки', {
            'fields': (('link_git', 'link_site'),)
        }),

    )
    inlines = (CardProjectInline,)


admin.site.register(Project, AdminProject)
