from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from shop.models import Item
from promocodes.models import PromoCode
from .serializers import (
    OrderSerializer,
    OrderItemSerializer
)
from ..models import (
    Order,
    OrderItem
)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
