from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Item, Manufactor


class TestManufactorView(TestCase):
    def test_manufactor_create_view(self):
        post_data = {'name': 'test manufactor name',
                     'summary': 'test manufactor summary'}
        response = self.client.post(reverse('manufactor_create'), data=post_data, follow=True)
        self.assertEqual(Manufactor.objects.count(), 3)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('/catalog/manufactor/3' in str(response.context))

    def test_manufactor_update_view(self):
        manufactor = Manufactor.objects.create(name='test name',
                                               summary='test summary')
        post_data = {'name': 'test update name',
                     'summary': 'test update summary'}
        response = self.client.post(reverse('manufactor_update', kwargs={'pk': manufactor.pk}),
                                    data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('test update name' in str(response.content))

    def test_manufactor_delete_view(self):
        manufactor = Manufactor.objects.create(name='test name',
                                               summary='test summary')
        response = self.client.post(reverse('manufactor_delete', kwargs={'pk': manufactor.pk}),
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('test name' not in str(response.context['object_list']))
        self.assertTrue('/catalog/manufactors' in str(response.context))


class TestCategoryView(TestCase):
    def test_category_create_view(self):
        post_data = {'name': 'test category name',
                     'summary': 'test category summary',
                     'availability': True}
        response = self.client.post(reverse('category_create'), data=post_data, follow=True)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('/catalog/category/1' in str(response.context))

    def test_category_update_view(self):
        category = Category.objects.create(name='test name',
                                           summary='test summary',
                                           availability=True)
        post_data = {'name': 'test update name',
                     'summary': 'test update summary'}
        response = self.client.post(reverse('category_update', kwargs={'pk': category.pk}), data=post_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('test update name' in str(response.content))

    def test_category_delete_view(self):
        category = Category.objects.create(name='test name',
                                           summary='test summary',
                                           availability=True)
        response = self.client.post(reverse('category_delete', kwargs={'pk': category.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('test name' not in str(response.context['object_list']))
        self.assertTrue('/catalog/categories' in str(response.context))
