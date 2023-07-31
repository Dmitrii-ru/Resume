from django.contrib import admin
from django.db.models import Sum
from mptt_blog import forms
from .models import *

admin.site.register(MyEducation)
admin.site.register(AboutMe)
admin.site.register(EmailSend)
admin.site.register(Feedback)

@admin.register(UniqueIP)
class AdminUniqueIP(admin.ModelAdmin):

    ordering = ['-count_visit']
    list_display = ('ip_address', 'count_visit', 'date')
    list_per_page = 50
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False





@admin.register(Stack)
class AdminSteck(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class CardProjectInline(admin.StackedInline):
    model = CardProject
    extra = 3


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
admin.site.register(EmailSettings)
