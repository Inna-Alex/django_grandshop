import pytest
import uuid

from django.urls import reverse

from catalog.forms import IssueForm
from catalog.models import Category, Item, Manufactor
from users.models import CustomUser

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def test_password():
    return 'test-pwd'


@pytest.fixture
def create_user(db, test_password):
    return CustomUser.objects.create_user(email='test@test.ru', password=test_password)


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user
        client.login(email=user.email, password=test_password)
        return client, user
    return make_auto_login


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


@pytest.fixture
def create_manufactor_params(db):
    def make_params(**kwargs):
        kwargs['name'] = 'test manufactor name params'
        kwargs['summary'] = 'test manufactor summary params'
        return kwargs
    return make_params


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

    def test_manufactor_create_view(self, db, client):
        url = reverse('manufactor_create')
        response = client.get(url)
        assert response.status_code == 200

    def test_manufactor_update_view(self, db, client, create_manufactor):
        manufactor = create_manufactor
        url = reverse('manufactor_update', kwargs={'pk': manufactor.pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_manufactor_delete_view(self, db, client, create_manufactor):
        manufactor = create_manufactor
        url = reverse('manufactor_delete', kwargs={'pk': manufactor.pk})
        response = client.get(url)
        assert response.status_code == 200


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

    def test_categories_raw_one_view(self, db, client, create_category):
        category = create_category
        response = client.get(reverse('categories_raw_one', kwargs={'pk': category.pk}))
        assert response.status_code == 200

    def test_categories_raw_by_func(self, db, client):
        response = client.get(reverse('categories_raw_by_func'))
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

    def test_category_create_view(self, db, client):
        url = reverse('category_create')
        response = client.get(url)
        assert response.status_code == 200

    def test_category_update_view(self, db, client, create_category):
        category = create_category
        url = reverse('category_update', kwargs={'pk': category.pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_category_delete_view(self, db, client, create_category):
        category = create_category
        url = reverse('category_delete', kwargs={'pk': category.pk})
        response = client.get(url)
        assert response.status_code == 200


@pytest.fixture
def create_item(db, create_manufactor, create_category):
    return Item.objects.create(manufactor=create_manufactor,
                               category=create_category,
                               name='Test item',
                               summary='Test item summary',
                               price=100,
                               availability=True,
                               quantity=10)


@pytest.fixture
def create_item_params(db, create_manufactor, create_category):
    def make_params(**kwargs):
        kwargs['manufactor'] = create_manufactor
        kwargs['category'] = create_category
        kwargs['summary'] = 'test item summary'
        kwargs['availability'] = True
        if 'name' not in kwargs:
            kwargs['name'] = 'test item name'
        if 'price' not in kwargs:
            kwargs['price'] = 100
        if 'quantity' not in kwargs:
            kwargs['quantity'] = 10
        return kwargs
    return make_params


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

    def test_item_object_create(self, db, client, create_item):
        item = create_item
        url = reverse('item_detail', kwargs={'pk': item.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert 'Test item' in str(response.content)

    def test_item_create_view(self, db, client):
        url = reverse('item_create')
        response = client.get(url)
        assert response.status_code == 200

    def test_item_update_view(self, db, client, create_item):
        item = create_item
        url = reverse('item_update', kwargs={'pk': item.pk})
        response = client.get(url)
        assert response.status_code == 200

    def test_item_delete_view(self, db, client, create_item):
        item = create_item
        url = reverse('item_delete', kwargs={'pk': item.pk})
        response = client.get(url, follow=True)
        assert response.status_code == 200

    def test_item_counter_redirect_view(self, db, client, create_item):
        item = create_item
        url = reverse('item_counter', kwargs={'pk': item.pk})
        url_redirect = '/catalog/item/{0}'.format(item.pk)
        response = client.get(url, follow=True)
        assert response.status_code == 200
        assert url_redirect in str(response.context)

    def test_items_to_csv_view(self, db, client, create_item):
        url = reverse('items_to_csv')
        response = client.get(url)
        assert response.status_code == 200

    def test_item_create_form_invalid_price(self, db, client, create_item_params):
        response = client.post(reverse('item_create'), data=create_item_params(price=0))
        assert response.status_code == 200
        assert 'Enter a number' in str(response.content)

    def test_item_create_form_invalid_quantity(self, db, client, create_item_params):
        response = client.post(reverse('item_create'), data=create_item_params(quantity=-1))
        assert response.status_code == 200
        assert 'Enter a whole number' in str(response.content)

    def test_items_news_list_returns_one_thing(self, db, client, create_item):
        url = reverse('item_news')
        response = client.get(url)
        data = response.context['item_list']
        assert response.status_code == 200
        assert len(data) == 1


class TestOrderView:
    def test_orders_redirect_if_not_logged_in(self, db, client):
        url = reverse('orders')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == '/accounts/login/?next=/catalog/orders/'


class TestItemIssueView:
    def test_item_issue_form_valid(self, db, create_item):
        item = create_item
        form = IssueForm(data={'select_item': item.pk})
        assert form.is_valid() is True

    def test_item_issue_form_invalid(self, db):
        item_id = uuid.uuid4
        form = IssueForm(data={'select_item': item_id})
        assert form.is_valid() is False

    def test_item_issue_redirect_if_not_logged_in(self, db, client):
        url = reverse('item_issue_send')
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == '/accounts/login/?next=/catalog/items/send_issue/'

    def test_item_issue_create_view_if_logged_in(self, db, create_item, auto_login_user):
        client, user = auto_login_user()
        url = reverse('item_issue_send')
        response = client.get(url)
        assert response.status_code == 200
        assert 'Test item' in str(response.content)
