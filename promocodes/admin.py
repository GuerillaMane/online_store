from django.contrib import admin
from .models import PromoCode


# Register your models here.


class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'is_active']
    list_filter = ['is_active', 'valid_from', 'valid_to']
    search_fields = ['code']


admin.site.register(PromoCode, PromoCodeAdmin)
