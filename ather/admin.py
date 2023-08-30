from django.contrib import admin
from .models import Person


class AdminPerson(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Person, AdminPerson)
