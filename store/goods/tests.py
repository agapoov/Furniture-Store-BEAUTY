from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from .models import Products, Categories


class CatalogViewTests(TestCase):
    def setUp(self):
        category1 = Categories.objects.create(name='Category 1', slug='category-1')
        category2 = Categories.objects.create(name='Category 2', slug='category-2')
        Products.objects.create(name='Product 1', category=category1, discount=0)
        Products.objects.create(name='Product 2', category=category1, discount=10)
        Products.objects.create(name='Product 3', category=category2, discount=0)

    def test_view_all_products(self):
        """Отображение всех продуктов"""
        response = self.client.get(reverse('catalog:index', kwargs={'category_slug': 'all'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')

    def test_view_products_by_category(self):
        """Отображение продуктов по категории"""
        response = self.client.get(reverse('catalog:index', kwargs={'category_slug': 'category-2'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 3')
        self.assertNotContains(response, 'Product 1')

    def test_view_non_existing_category(self):
        """Не существующая категория"""
        response = self.client.get(reverse('catalog:index', kwargs={'category_slug': 'non_existing'}))
        self.assertEqual(response.status_code, 404)


