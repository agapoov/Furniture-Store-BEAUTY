from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Categories, Products
from .utils import q_search


class CatalogViewTests(TestCase):
    def setUp(self):
        category1 = Categories.objects.create(name='Category 1', slug='category-1')
        category2 = Categories.objects.create(name='Category 2', slug='category-2')
        Products.objects.create(name='Product 1', category=category1, discount=0)
        Products.objects.create(name='Product 2', category=category1, discount=10)
        Products.objects.create(name='Product 3', category=category2, discount=0)

    def test_view_all_products(self):
        """Testing all products view"""
        response = self.client.get(reverse('catalog:index', kwargs={'category_slug': 'all'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')
        self.assertContains(response, 'Product 2')

    def test_view_products_by_category(self):
        """Testing product by category view"""
        response = self.client.get(reverse('catalog:index', kwargs={'category_slug': 'category-2'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 3')
        self.assertNotContains(response, 'Product 1')

    def test_view_non_existing_category(self):
        """Testing non-existing category"""
        response = self.client.get(reverse('catalog:index', kwargs={'category_slug': 'non_existing'}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class QsearchUtilsTests(TestCase):
    def setUp(self):
        self.category = Categories.objects.create(name='Бытовая техника')

        self.product1 = Products.objects.create(
            id=123, name='Кофемашина', slug='coffeemachine',
            description='Отличная кофемашина для дома',
            category=self.category
        )
        self.product2 = Products.objects.create(
            id=124, name='Чайник', slug='kettle',
            description='Электрический чайник на 1.5 литра',
            category=self.category
        )
        self.product3 = Products.objects.create(
            id=125, name='Кофе', slug='coffee',
            description='Ароматный молотый кофе',
            category=self.category
        )

    def test_search_by_id(self):
        """Testing search by id"""
        result = q_search('123')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.product1)

    def test_search_by_name(self):
        """Testing search by name"""
        result = q_search('Кофе')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.product3)

    def test_search_by_description(self):
        """Testing search by description"""
        result = q_search('электрический')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.product2)

    def test_no_results(self):
        """Testing no results"""
        result = q_search('ничего')
        self.assertEqual(len(result), 0)

    def test_invalid_id_length(self):
        """Testing too large id length"""
        result = q_search('123456')
        self.assertEqual(len(result), 0)
