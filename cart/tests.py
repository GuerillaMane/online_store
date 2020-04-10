from django.test import TestCase, Client, RequestFactory
from .cart import Cart
from promocodes.models import PromoCode
from shop.models import (
    Item,
    Shop,
    Category
)
from datetime import datetime
from django.contrib.auth.models import User


# Create your tests here.

class TestCart(TestCase):
    def setUp(self):
        self.shop = Shop.objects.create(
            name='shop',
            address='address',
            staff_amount=50
        )
        self.category = Category.objects.create(
            name='category',
            slug='category'
        )
        self.item = Item.objects.create(
            category=self.category,
            shop=self.shop,
            name='test_item',
            description='test',
            price=1.00,
            slug='test_item',
            stock=10,
            available=True,
            created=datetime.now(),
            updated=datetime.now()
        )
        self.new_item = Item.objects.create(
            category=self.category,
            shop=self.shop,
            name='new_item',
            description='some_new_description',
            price=100.2,
            slug='new_item',
            stock=5,
            available=True,
            created=datetime.now(),
            updated=datetime.now()
        )
        self.promocode = PromoCode.objects.create(
            code='test_code',
            valid_from='2019-12-31T23:59:36Z',
            valid_to='2020-12-31T23:59:36Z',
            discount=50,
            is_active=True
        )
        self.client = Client()
        self.request = RequestFactory()
        self.request.user = User()
        self.request.session = {'modified': True}

        self.cart = Cart(self.request)

    def test_cart_init(self):
        self.assertEqual({}, self.cart.cart)

    def test_cart_promocode_applying(self):
        self.cart.promocode_id = self.promocode.id
        self.assertEqual(50, self.cart.promocode.discount)
        self.assertEqual('test_code', self.cart.promocode.code)

    def test_cart_add_one_item(self):
        self.cart.add(self.item)
        # getting key from dictionary with one pair
        self.assertEqual(str(self.item.id), self.cart.cart.keys().__iter__().__next__())
        self.assertEqual(1, self.cart.cart[str(self.item.id)]['quantity'])
        self.assertEqual(str(self.item.price), self.cart.cart[str(self.item.id)]['price'])

    def test_cart_add_same_items(self):
        for q in range(5):
            self.cart.add(self.item)
        self.assertEqual(str(self.item.id), self.cart.cart.keys().__iter__().__next__())
        self.assertEqual(5, self.cart.cart[str(self.item.id)]['quantity'])
        self.assertEqual(str(self.item.price), self.cart.cart[str(self.item.id)]['price'])

    def test_cart_add_different_items(self):
        for q in range(2):
            self.cart.add(self.item)
            self.cart.add(self.new_item)
        self.assertEqual(2, self.cart.cart.__len__())
        self.assertEqual(2, self.cart.cart[str(self.new_item.id)]['quantity'])
        self.assertEqual(str(self.new_item.price), self.cart.cart[str(self.new_item.id)]['price'])

    def test_remove_cart_w_one_item(self):
        self.cart.add(self.item)
        self.cart.remove(self.item)
        self.assertEqual({}, self.cart.cart)

    def test_remove_cart_w_two_items(self):
        self.cart.add(self.item)
        self.cart.add(self.new_item)
        self.cart.remove(self.item)
        self.assertEqual(1, self.cart.cart.__len__())
        self.assertEqual('2', self.cart.cart.keys().__iter__().__next__())

    def test_cart_len(self):
        self.cart.add(self.item, quantity=5)
        self.cart.add(self.new_item, quantity=5)
        self.assertEqual(10, self.cart.__len__())

    def test_cart_get_total_price(self):
        self.cart.add(self.item, quantity=2)
        self.cart.add(self.new_item, quantity=2)
        tmp_total = self.item.price * 2 + self.new_item.price * 2
        # change to float, 'cause get_total_price returns Decimal
        self.assertEqual(tmp_total, float(self.cart.get_total_price()))

    def test_cart_wo_code_get_discount(self):
        self.assertEqual(0, int(self.cart.get_discount()))

    def test_cart_get_discount(self):
        self.cart.promocode_id = self.promocode.id
        self.cart.add(self.item, quantity=5)
        self.assertEqual(2.50, float(self.cart.get_discount()))

    def test_cart_get_discount_total_price(self):
        self.cart.promocode_id = self.promocode.id
        self.cart.add(self.item, quantity=10)
        self.assertEqual(5.00, float(self.cart.get_discount_total_price()))
