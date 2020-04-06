from django.db import models
from django.urls import reverse
from PIL import Image


# Create your models here.


class Shop(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Наименование магазина'
    )
    address = models.CharField(
        max_length=256,
        verbose_name='Адрес магазина'
    )
    staff_amount = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name} {self.address}'

    def get_absolute_url(self):
        return reverse('shop:shop_update', args=(self.id,))

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = "Магазины"
        ordering = (
            'name',
        )


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=200,
        db_index=True,
        unique=True
    )
    is_delete = models.BooleanField(
        default=False,
        verbose_name='Удалено'
    )

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()

    def save(self, *args, **kwargs):
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('shop:item_list_by_category',
    #                    args=[self.slug])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = (
            'name',
        )


class Item(models.Model):
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Категория',
    )
    shop = models.ForeignKey(
        'Shop',
        on_delete=models.CASCADE,
        verbose_name='Магазин'
    )
    name = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name='Наименование товара'
    )
    description = models.TextField(
        max_length=1024,
        verbose_name='Описание товара'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена'
    )
    item_picture = models.ImageField(
        upload_to='uploads/shop/items/%Y/%m/%d',
        default=None,
        null=True,
        blank=True,
        verbose_name='Изображение предмета'
    )
    slug = models.SlugField(
        max_length=200,
        db_index=True
    )
    stock = models.PositiveIntegerField()
    available = models.BooleanField(
        default=True,
        verbose_name='Есть на складе'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('shop_app:item_update', args=(self.id,))

    def save(self, *args, **kwargs):
        try:
            this_entry = Item.objects.get(id=self.id)
            if this_entry.item_picture != self.item_picture:
                this_entry.item_picture.delete(save=False)
        except:
            pass
        super(Item, self).save(*args, **kwargs)
        if self.item_picture:
            image = Image.open(self.item_picture.path)
            max_size = max(image.size[0], image.size[1])
            multiplier = max_size / 1200
            image = image.resize((round(image.size[0] / multiplier), round(image.size[1] / multiplier)),
                                 Image.ANTIALIAS)
            image.save(self.item_picture.path)
            print(image.size)

            image.save(self.item_picture.path)

    def delete(self, *args, **kwargs):
        self.item_picture.delete(save=False)
        super(Item, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:item_detail', args=[self.id, self.slug])

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = (
            'name',
        )
        index_together = (
            ('id', 'slug'),
        )
