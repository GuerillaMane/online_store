from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import (
    Item,
    Shop,
    Category,
)
from .forms import (
    ItemForm,
    ShopForm,
    CategoryForm,
)
from cart.forms import CartAddForm


# Create your views here.


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('profile_app:login')
    template_name = 'shop/base.html'


class ItemListView(ListView):
    template_name = 'shop/item/item_list.html'
    model = Item
    context_object_name = 'item_list'
    paginate_by = 3

    def get_queryset(self):
        return Item.objects.filter(available=True)

    def get_paginate_by(self, queryset):
        page_number = self.request.GET.get('page_number')
        if page_number is not None:
            self.paginate = page_number
        return super(ItemListView, self).get_paginate_by(self.get_queryset())

    def get(self, request, *args, **kwargs):
        return super(ItemListView, self).get(request, *args, **kwargs)


def item_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    items = Item.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=category)
    return render(request, 'shop/item/list.html',
                  {'category': category,
                   'categories': categories,
                   'items': items})


def item_detail(request, id, slug):
    item = get_object_or_404(Item, id=id, slug=slug, available=True)
    cart_form = CartAddForm()
    return render(request, 'shop/item/item_detail.html', {'item': item, 'cart_form': cart_form})


class ItemCreate(CreateView):
    template_name = 'shop/item/item_create.html'
    model = Item
    form_class = ItemForm


class ItemUpdate(UpdateView):
    template_name = 'shop/item/item_create.html'
    model = Item
    form_class = ItemForm


class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('shop:item_list')
    template_name = 'shop/confirm_delete.html'
