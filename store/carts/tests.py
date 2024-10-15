from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from carts.models import Cart
from goods.models import Categories, Products
from users.models import User


class CartAddViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test-username',
            password='JustPasswordAndNothingElse',
            email='example@gmailc.com'
        )
        category1 = Categories.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Products.objects.create(
            name='test-product',
            price=10.0,
            category=category1
        )
        self.add_to_cart_url = reverse('cart:cart_add')

    def test_add_to_cart(self):
        """Test that we can add a product to the cart"""
        self.client.login(username='test-username', password='JustPasswordAndNothingElse')

        response = self.client.post(
            self.add_to_cart_url,
            {'product_id': self.product.id},
            **{'HTTP_REFERER': reverse('orders:create-order')}
        )

        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['message'], 'Товар добавлен в корзину')
        self.assertIn('<div', response_data['cart_items_html'])


