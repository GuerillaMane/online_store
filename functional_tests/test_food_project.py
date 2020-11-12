from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.ui import Select
import time


class TestFoodProject(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(
            executable_path=r'D:\Учеба\TeachMeSkills\online_store\online_store\functional_tests\geckodriver.exe'
        )
        self.browser.get('http://127.0.0.1:8000/profile/login/')
        self.browser.find_element_by_id('id_username').send_keys('guerilla')
        self.browser.find_element_by_id('id_password').send_keys('Sebese43')
        self.browser.find_element_by_id('sub_btn').click()

    def tearDown(self):
        self.browser.close()

    def test_auth_display(self):
        # self.browser.get(self.live_server_url)
        self.browser.get('http://127.0.0.1:8000/profile/login/')
        alert = self.browser.find_element_by_class_name('form-group')
        self.assertEquals(
            alert.find_element_by_tag_name('label').text,
            'Username'
        )

    def test_auth_success(self):
        expected_url = 'http://127.0.0.1:8000/'
        self.browser.get('http://127.0.0.1:8000/profile/login/')
        self.browser.find_element_by_id('id_username').send_keys('guerilla')
        self.browser.find_element_by_id('id_password').send_keys('Sebese43')
        self.browser.find_element_by_id('sub_btn').click()
        assert self.browser.current_url == expected_url

    def test_auth_error(self):
        self.browser.get('http://127.0.0.1:8000/profile/login/')
        self.browser.find_element_by_id('id_username').send_keys('fafa')
        self.browser.find_element_by_id('id_password').send_keys('228')
        self.browser.find_element_by_id('sub_btn').click()
        alert = self.browser.find_element_by_class_name('row')
        self.assertEquals(
            alert.find_element_by_tag_name('p').text,
            'Password or Username is not correct'
        )

    def test_add_shop(self):
        self.browser.find_element_by_link_text('Shops').click()
        self.browser.find_element_by_link_text('Add Shop').click()
        self.browser.find_element_by_id('id_name').send_keys('Фрикаделька')
        self.browser.find_element_by_id('id_address').send_keys('ул. Цаля')
        self.browser.find_element_by_id('id_staff_amount').send_keys('300')
        time.sleep(3)
        self.browser.find_element_by_class_name('row').find_element_by_tag_name('button').click()
        time.sleep(1)
        self.assertEquals(
            self.browser.find_element_by_class_name('row').find_element_by_tag_name('button').text,
            'Update'
                          )
        alert = self.browser.find_element_by_class_name('row')
        self.assertEquals(
            alert.find_element_by_tag_name('a').text,
            'Delete'
        )

    def test_add_shop_negative(self):
        self.browser.find_element_by_link_text('Shops').click()
        self.browser.find_element_by_link_text('Add Shop').click()
        self.browser.find_element_by_id('id_name').send_keys('Молоко')
        time.sleep(3)
        self.browser.find_element_by_class_name('row').find_element_by_tag_name('button').click()
        self.assertEquals(
            self.browser.find_element_by_class_name('row').find_element_by_tag_name('button').text,
            'Save'
        )

    def test_add_item(self):
        self.browser.find_element_by_link_text('Items').click()
        self.browser.find_element_by_link_text('Add Item').click()
        Select(self.browser.find_element_by_id('id_category')).select_by_visible_text('Еда')
        Select(self.browser.find_element_by_id('id_shop')).select_by_visible_text('af af')
        self.browser.find_element_by_id('id_name').send_keys('Фрикаделька')
        self.browser.find_element_by_id('id_description').send_keys('фафафа')
        self.browser.find_element_by_id('id_price').send_keys('300')
        self.browser.find_element_by_id('id_slug').send_keys('frikadelka')
        self.browser.find_element_by_id('id_stock').send_keys('5')
        time.sleep(3)
        self.browser.find_element_by_class_name('row').find_element_by_tag_name('button').click()
        self.assertEquals(
            self.browser.find_element_by_class_name('row').find_element_by_tag_name('h2').text,
            'Фрикаделька'
        )

    def test_add_item_negative(self):
        self.browser.find_element_by_link_text('Items').click()
        self.browser.find_element_by_link_text('Add Item').click()
        Select(self.browser.find_element_by_id('id_category')).select_by_visible_text('Еда')
        Select(self.browser.find_element_by_id('id_shop')).select_by_visible_text('af af')
        self.browser.find_element_by_id('id_description').send_keys('фафафа')
        self.browser.find_element_by_id('id_price').send_keys('300')
        self.browser.find_element_by_id('id_slug').send_keys('frikadelka')
        self.browser.find_element_by_id('id_stock').send_keys('5')
        time.sleep(3)
        self.browser.find_element_by_class_name('row').find_element_by_tag_name('button').click()
        self.assertEquals(
            self.browser.find_element_by_class_name('row').find_element_by_tag_name('button').text,
            'Save'
        )

    def test_add_cart(self):
        self.browser.find_element_by_link_text('Items').click()
        self.browser.find_element_by_link_text('Капучино').click()
        Select(self.browser.find_element_by_id('id_quantity')).select_by_visible_text('2')
        self.browser.find_element_by_id('id_add').click()
        self.assertEquals(
            self.browser.find_element_by_class_name('row').find_element_by_tag_name('h1').text,
            'Your Cart'
        )

    def test_add_promocode(self):
        self.browser.find_element_by_link_text('Profile').click()
        self.browser.find_element_by_link_text('Available Promocodes for You').click()
        self.browser.find_element_by_link_text('Add Promocode').click()
        self.browser.find_element_by_id('id_code').send_keys('Keki4')
        self.browser.find_element_by_id('id_valid_from').send_keys('19.03.2020 14:42:48')
        self.browser.find_element_by_id('id_valid_to').send_keys('19.07.2020 14:42:48')
        self.browser.find_element_by_id('id_discount').send_keys('50')
        self.browser.find_element_by_id('id_is_active').click()
        self.browser.find_element_by_class_name('row').find_element_by_tag_name('button').click()
        time.sleep(2)
        self.assertEquals(
            self.browser.find_element_by_class_name('row').find_element_by_tag_name('button').text,
            'Update'
        )

    def test_home(self):
        self.browser.find_element_by_link_text('Home').click()
        alert = self.browser.find_element_by_tag_name('img')
        time.sleep(5)
        self.assertEquals(
            alert.get_attribute('src'),
            'http://127.0.0.1:8000/static/shop/pictures/bebe.png'
        )
