import pytest

from django.contrib.auth.models import User
from django.urls import reverse

from catalog.models import Category, Manufactor

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def create_manufactor(db):
    return Manufactor.objects.create(name='Test manufactor', summary='Test manufactor summary')


@pytest.fixture
def create_manufactor_by_name(db):
    def make_manufactor(**kwargs):
        kwargs['summary'] = 'test manufactor summary'
        if 'name' not in kwargs:
            kwargs['name'] = 'test manufactor name'
        return Manufactor.objects.create(**kwargs)
    return make_manufactor


class TestManufactoryView:
    def test_manufactors_returns_list_two_things(self, db, client):
        response = client.get(reverse('manufactors'))
        data = response.context['manufactor_list']
        assert response.status_code == 200
        assert len(data) == 2

    def test_manufactor_url_create(self, db, client):
        response = client.get(reverse('manufactor_create'))
        assert response.status_code == 200

    def test_manufactor_object_create(self, db, client, create_manufactor):
        manufactor = create_manufactor
        url = reverse('manufactor_detail', kwargs={'pk': manufactor.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert 'Test manufactor' in str(response.content)

    def test_manufactor_object_create_by_name(self, db, client, create_manufactor_by_name):
        manufactor = create_manufactor_by_name(name='test name')
        url = reverse('manufactor_detail', kwargs={'pk': manufactor.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert 'test name' in str(response.content)


@pytest.fixture
def create_category(db):
    return Category.objects.create(name='Test category', summary='Test category summary',
                                   availability=True)


@pytest.fixture
def create_category_by_name(db):
    def make_category(**kwargs):
        kwargs['summary'] = 'test category summary'
        if 'name' not in kwargs:
            kwargs['name'] = 'test category name'
        return Category.objects.create(**kwargs)
    return make_category


class TestCategoryView:
    def test_categories_returns_empty_list(self, db, client):
        response = client.get(reverse('categories'))
        data = response.context['category_list']
        assert response.status_code == 200
        assert '<QuerySet []>' == str(data)

    def test_categories_raw_view_list(self, db, client):
        response = client.get(reverse('categories_raw'))
        assert response.status_code == 200

    def test_categories_raw_all_view_list(self, db, client):
        response = client.get(reverse('categories_raw_all'))
        assert response.status_code == 200

    def test_category_object_create(self, db, client, create_category):
        category = create_category
        url = reverse('category_detail', kwargs={'pk': category.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert 'Test category' in str(response.content)

    def test_category_object_create_by_name(self, db, client, create_category_by_name):
        category = create_category_by_name(name='test name')
        url = reverse('category_detail', kwargs={'pk': category.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert 'test name' in str(response.content)


class TestItemView:
    def test_items_returns_empty_list(self, db, client):
        response = client.get(reverse('items'))
        data = response.context['item_list']
        assert response.status_code == 200
        assert '<QuerySet []>' == str(data)

    def test_items_news_list_view(self, db, client):
        response = client.get(reverse('item_news'))
        assert response.status_code == 200

    def test_items_ne_filter_list_view(self, db, client):
        response = client.get(reverse('item_ne'))
        assert response.status_code == 200

    def test_items_quantity_abs_filter_list_view(self, db, client):
        response = client.get(reverse('item_abs'))
        assert response.status_code == 200

