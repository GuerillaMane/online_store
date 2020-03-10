from django import forms
from .models import (
    Item,
    Shop,
    Category,
)


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
