from rest_framework import serializers
from ..models import (
    Item,
    Shop,
    Category,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    category_obj = CategorySerializer(
        source='category',
        read_only=True,
    )
    shop_obj = ShopSerializer(
        source='shop',
        read_only=True,
    )

    class Meta:
        model = Item
        exclude = ('category', 'shop')
