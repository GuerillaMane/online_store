from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    TemplateView,
)
from .models import (
    Item,
    Shop,
    Category,
)


# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('profile_app:login')
    template_name = 'shop/base.html'


class ItemListView(ListView):
    template_name = 'shop/item_list.html'
    model = Item
    context_object_name = 'item_list'
    paginate_by = 3

    def get_queryset(self):
        return Item.objects.all()

    def get_paginate_by(self, queryset):
        page_number = self.request.GET.get('page_number')
        if page_number is not None:
            self.paginate = page_number
        return super(ItemListView, self).get_paginate_by(self.get_queryset())

    def get(self, request, *args, **kwargs):
        return super(ItemListView, self).get(request, *args, **kwargs)
