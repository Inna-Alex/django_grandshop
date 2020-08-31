import pytest

from django.contrib.auth.models import User
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


class TestManufactoryView:
    def test_manufactors_returns_empty_list(self, db, client):
        response = client.get(reverse('manufactors'))
        data = response.context['manufactor_list']
        assert response.status_code == 200
        assert len(data) == 2


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

