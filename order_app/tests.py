from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User
from .models import (
    Order
)
from .forms import OrderCreateForm
from shop.models import (
    Item,
    Shop,
    Category
)
from promocodes.models import PromoCode
from cart.cart import Cart

# Create your tests here.


class TestOrder(TestCase):
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
        # self.request.user = User()
        self.request.session = {'modified': True}

        self.user = User.objects.create(
            username='admin',
            password='admin',
            is_superuser=True
        )

        self.order = Order.objects.create(
            client=self.user,
            address = 'test',
            phone_number = '80291112233'
        )

        self.cart = Cart(self.request)

    def test_order_create(self):
        # self.client.login(username='admin', password='admin')
        self.client.force_login(user=self.user)
        form_data = {
            'client': self.user,
            'address': 'test',
            'phone_number': '80291112233'
        }
        form = OrderCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.cart.add(self.item)
        response = self.client.post(reverse('order_app:order_create'), form_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_order_model_str(self):
        self.assertEqual(self.order.__str__(), f'Order {self.order.id}')

    def test_order_model_get_total_cost(self):
        self.assertEqual(int(self.order.get_total_cost()), 0)
