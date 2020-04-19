from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

# Create your models here.


class PromoCode(models.Model):
    code = models.CharField(
        max_length=20,
        unique=True
    )
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    is_active = models.BooleanField()

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('promocodes:promo_update', args=(self.id,))

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
