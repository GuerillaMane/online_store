from decimal import Decimal, ROUND_HALF_DOWN
from django.conf import settings
from shop.models import Item
from promocodes.models import PromoCode


class Cart(object):
    def __init__(self, request):
        # храним текущую сессию
        self.session = request.session
        # пытаемся получить корзину из текущей сессии
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранение пустой корзины в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.promocode_id = self.session.get('promocode_id')

    def add(self, item, quantity=1, update_quantity=False):
        # добавляем новый айтем либо обновляем его количество
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0,
                                  'price': str(item.price)}
        # булеан, который показывает, обновляем (True), или же добавляем к текущему (False)
        if update_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()

    def save(self):
        # обновляем сессию
        self.session[settings.CART_SESSION_ID] = self.cart
        # помечаем сессию как modified
        self.session['modified'] = True

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        item_ids = self.cart.keys()
        items = Item.objects.filter(id__in=item_ids)
        for item in items:
            self.cart[str(item.id)]['item'] = item

        for cart_item in self.cart.values():
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            yield cart_item

    def __len__(self):
        return sum(cart_item['quantity'] for cart_item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(cart_item['price']) * cart_item['quantity'] for cart_item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session['modified'] = True

    @property
    def promocode(self):
        if self.promocode_id:
            return PromoCode.objects.get(id=self.promocode_id)
        return None

    def get_discount(self):
        if self.promocode:
            discount = (self.promocode.discount / Decimal(100)) * self.get_total_price()
            return discount.quantize(Decimal("1.00"), ROUND_HALF_DOWN)
        return Decimal('0')

    def get_discount_total_price(self):
        return self.get_total_price() - self.get_discount()
