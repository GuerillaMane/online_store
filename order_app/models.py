from django.db import models
from decimal import Decimal, ROUND_HALF_DOWN
from django.core.validators import MinValueValidator, MaxValueValidator
from shop.models import Item
from django.contrib.auth.models import User
from promocodes.models import PromoCode


# Create your models here.


class Order(models.Model):
    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    address = models.CharField(
        max_length=256,
        verbose_name='Адрес доставки'
    )
    phone_number = models.CharField(
        max_length=32,
        null=True,
        verbose_name='Номер телефона'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    paid = models.BooleanField(
        default=False
    )

    promocode = models.ForeignKey(
        PromoCode,
        on_delete=models.DO_NOTHING,
        related_name='orders',
        null=True,
        blank=True
    )
    discount = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = (
            '-created',
        )
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - (total_cost * (self.discount / Decimal('100'))).quantize(Decimal("1.00"), ROUND_HALF_DOWN)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.DO_NOTHING
    )
    item = models.ForeignKey(
        Item,
        related_name='order_items',
        on_delete=models.DO_NOTHING
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
