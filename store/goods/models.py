from django.db import models
from django.urls import reverse


class Categories(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=256, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False)
    slug = models.SlugField(max_length=256, unique=True, blank=True, null=True)
    description = models.TextField(max_length=1024, blank=True, null=True)
    image = models.ImageField(upload_to='goods_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(null=False, default=0)
    category = models.ForeignKey(Categories, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)

    def __str__(self):
        return f'{self.name} Количество - {self.quantity}'

    def get_absolute_url(self):
        return reverse('catalog:product', kwargs={'product_slug': self.slug})

    def display_id(self):
        return f'{self.id:05}'

    def sell_price(self):
        if self.discount > 0:
            return round(self.price - self.price * self.discount/100, 2)
        else:
            return self.price
