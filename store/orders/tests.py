from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from carts.models import Cart
from goods.models import Categories, Products
from orders.models import Order, OrderItem
from users.models import User

from unittest.mock import patch
from yookassa import Payment


class CreateOrderViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='UserPass1232')
        self.client.login(username='testuser', password='UserPass1232')

        self.category = Categories.objects.create(name='Test Category', slug='test-category')

        self.product = Products.objects.create(name='Test Product', quantity=10, price=100, category=self.category)

        Cart.objects.create(user=self.user, product=self.product, quantity=1)

        self.url = reverse('orders:create-order')

        self.order_data = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'phone_number': '1234567890',
            'requires_delivery': '1',  # YES
            'delivery_address': 'Test Address',
            'payment_on_get': '1'
        }

    def test_get_initial_data(self):
        """Testing for display of initial values"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.email)

    def test_create_order_success(self):
        """Testing for successful creation of order"""
        response = self.client.post(self.url, self.order_data)
        self.assertRedirects(response, reverse('users:profile'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_product_quantity_decreases_after_order(self):
        """Testing for decreasing quantity after order"""
        init_quantity = self.product.quantity
        self.assertEqual(init_quantity, 10)
        response = self.client.post(self.url, self.order_data)
        self.assertRedirects(response, reverse('users:profile'))

        product = Products.objects.get(id=self.product.id)

        self.assertEqual(product.quantity, init_quantity-1)

    def test_out_of_stock_product(self):
        """Testing for out of stock product"""
        Cart.objects.filter(user=self.user).update(quantity=25)
        response = self.client.post(self.url, self.order_data)

        self.assertRedirects(response, self.url)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "['Недостаточное кол-во товара Test Product на складе. В наличии: 10']")
