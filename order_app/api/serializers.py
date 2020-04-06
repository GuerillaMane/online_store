from rest_framework import serializers
from profile_app.api.serializers import UserSerializer
from promocodes.api.serializers import PromoCodeSerializer
from shop.api.serializers import ItemSerializer
from ..models import (
    Order,
    OrderItem
)


class OrderSerializer(serializers.ModelSerializer):
    client_obj = UserSerializer(
        source='client',
        read_only=True
    )
    promocode_obj = PromoCodeSerializer(
        source='promocode',
        read_only=True
    )

    class Meta:
        model = Order
        exclude = ('client', 'promocode')


class OrderItemSerializer(serializers.ModelSerializer):
    order_obj = OrderSerializer(
        source='order',
        read_only=True
    )
    item_obj = ItemSerializer(
        source='item',
        read_only=True
    )

    class Meta:
        model = OrderItem
        exclude = ('order', 'item')
