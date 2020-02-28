from django.contrib import admin
from .models import (
    Item,
    Shop,
    Category,
)

# Register your models here.

admin.site.register(Item)
admin.site.register(Shop)
admin.site.register(Category)
