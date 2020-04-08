from django.test import TestCase
# на базе UnitTest, от этого класса наследуем все классы для тестирования
# в тестах создается тестовая база данных в памяти и по завершению тест-кейсов удаляется
from .models import (
    Category,
    Shop,
    Item,
)
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse

# Create your tests here.

USERNAME = 'admin'
PASSWORD = 'admin'
LOGIN_URL = '/profile/login/'


class TestShop(TestCase):

    def setUp(self):
        self.shop = Shop.objects.create(
            name='my_shop',
            address='some_address',
            staff_amount=50
        )
        self.category = Category.objects.create(
            name='someCategory',
            slug='some_category'
        )
        self.item = Item.objects.create(
            category=self.category,
            shop=self.shop,
            name='test_item',
            description='some_description',
            price=100.67,
            slug='test_item',
            stock=10,
            available=True,
            created=datetime.now(),
            updated=datetime.now()
        )

        # self.item = Item()
        # self.item.department = self.department
        # self.item.description = 'someDescription'
        # self.item.price = 100.500
        # self.item.save()

        self.user = User.objects.create(
            username=USERNAME,
            is_superuser=True,
            password=PASSWORD
        )
        self.text_on_login_page = 'Username'

    def test_item_create(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})

        response = self.client.post('/item_create/', {
            'category': self.category.id,
            'shop': self.shop.id,
            'name': 'test_item',
            'description': 'tested item',
            'price': 101.2,
            'slug': 'test_item',
            'stock': 10,
            'available': True
        }, follow=True)

        self.assertEqual(response.status_code, 200)

        new_item = Item.objects.get(name='test_item', price=101.2)
        self.assertEqual(new_item.name, 'test_item')
        self.assertEqual(new_item.description, 'tested item')
        self.assertEqual(new_item.id, 2)

    def test_item_update(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})

        new_item = Item.objects.create(
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

        response = self.client.post(f'/item_update/{new_item.id}/', {
            'category': self.category.id,
            'shop': self.shop.id,
            'name': 'updated_item',
            'description': 'item was updated',
            'price': 101.2,
            'slug': 'upd_item',
            'stock': 6,
            'available': True,
            'created': datetime.now(),
            'updated': datetime.now()
        })
        # if you post to form, you have to post all required fields, not just the ones you are updating!

        self.assertEqual(response.status_code, 302)
        # UpdateView returns 302 code, not 200

        new_item.refresh_from_db()
        # need to reload new_item from the database after update
        self.assertEqual(new_item.name, 'updated_item')
        self.assertEqual(new_item.stock, 6)

    # in a DeleteView, the GET request returns a confirmation page, and POST request deletes the object
    def test_item_delete_get_request(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})

        response = self.client.get(f'/item_delete/{self.item.id}/', follow=True)
        self.assertContains(response, 'Вы действительно хотите удалить')

    def test_item_delete_post_request(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})

        response = self.client.post(f'/item_delete/{self.item.id}/', follow=True)
        self.assertRedirects(response, '/item_list/', status_code=302)

    def test_item_detail(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})

        response = self.client.get(f'/{self.item.id}/{self.item.slug}', follow=True)
        self.assertContains(response, self.item.name)
        self.assertContains(response, self.item.description)

    def test_item_list(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})

        new_item = Item.objects.create(
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
        not_available_item = Item.objects.create(
            category=self.category,
            shop=self.shop,
            name='tmp_item',
            description='some_tmp_description',
            price=100.2,
            slug='tmp_item',
            stock=0,
            available=False,
            created=datetime.now(),
            updated=datetime.now()
        )

        response = self.client.get(reverse('shop:item_list'))
        self.assertContains(response, self.item.name)
        self.assertContains(response, new_item.name)
        self.assertNotContains(response, not_available_item.name)

    def test_shop_create(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})

        response = self.client.post('/shop_create/', {
            'name': 'test_shop',
            'address': 'some_address',
            'staff_amount': 28
        }, follow=True)

        self.assertEqual(response.status_code, 200)

        new_shop = Shop.objects.get(name='test_shop')
        self.assertEqual(new_shop.staff_amount, 28)
        self.assertEqual(new_shop.address, 'some_address')
        self.assertEqual(new_shop.id, 2)
        self.assertTemplateUsed(response, 'shop/shop/shop_create.html')

    def test_shop_update(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})

        response = self.client.post(f'/shop_update/{self.shop.id}/', {
            'name': 'updated_shop',
            'address': 'updated_address',
            'staff_amount': 39
        })

        self.assertEqual(response.status_code, 302)

        self.shop.refresh_from_db()
        # need to reload new_item from the database after update
        self.assertEqual(self.shop.name, 'updated_shop')
        self.assertEqual(self.shop.staff_amount, 39)
        self.assertEqual(self.shop.address, 'updated_address')

    def test_shop_delete_get_request(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})

        response = self.client.get(f'/shop_delete/{self.shop.id}/', follow=True)
        self.assertContains(response, 'Вы действительно хотите удалить')

    def test_shop_delete_post_request(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})

        response = self.client.post(f'/shop_delete/{self.shop.id}/', follow=True)
        self.assertRedirects(response, '/shop_list/', status_code=302)

    def test_shop_detail(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})

        # response = self.client.post(f'/shop_info/{self.shop.id}/', follow=True)
        response = self.client.get(reverse('shop:shop_detail', kwargs={'pk': self.shop.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.shop.name)
        self.assertTemplateUsed(response, 'shop/shop/shop_detail.html')

    def test_shop_list(self):
        self.client.post(LOGIN_URL, {'username': USERNAME, 'password': PASSWORD})
        new_shop = Shop.objects.create(
            name='new_shop',
            address='new_address',
            staff_amount=39
        )

        response = self.client.get(reverse('shop:shop_list'))
        self.assertContains(response, self.shop.name)
        self.assertContains(response, new_shop.name)

    def test_category_model_delete(self):
        self.category.delete()
        self.assertEqual(self.category.is_delete, True)

    def test_category_model_str(self):
        self.assertEqual(self.category.name, self.category.__str__())

    def test_item_model_str(self):
        self.assertEqual(self.item.name, self.item.__str__())

    def test_shop_model_str(self):
        self.assertEqual(f'{self.shop.name} {self.shop.address}', self.shop.__str__())
