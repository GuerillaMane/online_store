from django.test import TestCase
from .models import PromoCode


class TestPromoCode(TestCase):
    def setUp(self):
        self.promocode = PromoCode.objects.create(
            code='test_code',
            valid_from='2019-12-31T23:59:36Z',
            valid_to='2020-12-31T23:59:36Z',
            discount=50,
            is_active=True
        )

    def test_promocode_model_str(self):
        self.assertEqual(self.promocode.code, self.promocode.__str__())
