from django.contrib import admin
from .models import Person, ImagesProductsShop


class PersonImageAdmin(admin.TabularInline):
    model = ImagesProductsShop
    extra = 1


class PersonAdmin (admin.ModelAdmin):
    inlines = [PersonImageAdmin]

admin.site.register(Person,PersonAdmin)
