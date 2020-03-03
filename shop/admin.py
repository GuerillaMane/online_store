from django.contrib import admin
from .models import (
    Item,
    Shop,
    Category,
)

# Register your models here.

admin.site.register(Shop)


class CategoryAdministration(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdministration)


class ItemAdministration(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Item, ItemAdministration)
