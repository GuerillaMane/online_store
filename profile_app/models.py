from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.


class Profile(models.Model):
    # создаём связь с моделью User
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        # когда удаляем Profile оставляем User
        verbose_name='Профиль пользователя'
    )
    address = models.CharField(
        max_length=512,
        verbose_name='Адрес пользователя',
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        max_length=24,
        verbose_name='Телефон пользователя',
        blank=True,
        null=True
    )
    birth_date = models.DateField(
        verbose_name='Дата рождения пользователя',
        null=True,
        blank=True
    )
    profile_picture = models.ImageField(
        upload_to='uploads/profile_app/profile_pics',
        default='uploads/profile_app/cute_kitten_face.png',
        blank=True,
        null=True
    )

    def __str__(self):
        print(self.__getattribute__('phone_number'))
        return f'{self.user.first_name} {self.user.email}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = (
            'user',
        )
