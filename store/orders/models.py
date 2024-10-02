from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from goods.models import Products
from users.models import User


class OrderItemQuerySet(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'В обработке'),
        ('paid', 'Оплачено'),
        ('shipped', 'Отправлено'),
        ('completed', 'Завершено'),
        ('canceled', 'Отменено'),
    ]

    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name='Пользователь', default=None)
    phone_number = PhoneNumberField(region='RU')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    requires_delivery = models.BooleanField(default=False, verbose_name='Требуется доставка')
    payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при получении')
    delivery_address = models.TextField(null=True, blank=True, verbose_name='Адрес доставки')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='processing', verbose_name='Статус заказа')
    payment_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='ID платежа')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

    def __str__(self):
        return f'Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(to=Products, on_delete=models.SET_DEFAULT, null=True, verbose_name='Продукт', default=None)
    name = models.CharField(max_length=120, verbose_name='Название')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Цена')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Проданный товар'
        verbose_name_plural = 'Проданные товары'

    objects = OrderItemQuerySet.as_manager()

    def products_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f'Товар {self.product.name} | Заказ {self.order.pk} | Пользователь {self.order.user.username}'
