import pytest
from django.utils.translation import gettext_lazy as _
import uuid

from catalog.models import Manufactor, Category, Item

pytestmark = [pytest.mark.django_db]

class TestManufactoryModel:
    @pytest.fixture
    def init_db(db):
        manufactor = Manufactor.objects.create(name='ASUS creator', summary='ASUS summary to be continue')

    def test_name_label(db, init_db):
        manufactor = Manufactor.objects.get(manufactor_id=1)
        field_label = manufactor._meta.get_field('name').verbose_name
        assert(field_label == _('Название'))

    def test_name_max_length(db, init_db):
        manufactor=Manufactor.objects.get(manufactor_id=1)
        max_length = manufactor._meta.get_field('name').max_length
        assert(max_length == 200)

    def test_summary_label(db, init_db):
        manufactor = Manufactor.objects.get(manufactor_id=1)
        field_label = manufactor._meta.get_field('summary').verbose_name
        assert(field_label == _('Описание'))

    def test_summary_max_length(db, init_db):
        manufactor=Manufactor.objects.get(manufactor_id=1)
        max_length = manufactor._meta.get_field('summary').max_length
        assert(max_length == 500)

    def test_get_absolute_url(db, init_db):
        manufactor=Manufactor.objects.get(manufactor_id=1)
        assert(manufactor.get_absolute_url() == '/catalog/manufactor/1')

class TestCategoryModel:
    @pytest.fixture
    def init_db(db):
        Category.objects.create(name='VR для домохозяек', summary='Когда-нибудь придумают... наверное...')

    def test_name_label(db, init_db):
        category = Category.objects.get(category_id=1)
        field_label = category._meta.get_field('name').verbose_name
        assert(field_label == _('Название'))

    def test_name_max_length(db, init_db):
        category=Category.objects.get(category_id=1)
        max_length = category._meta.get_field('name').max_length
        assert(max_length== 200)

    def test_summary_label(db, init_db):
        category = Category.objects.get(category_id=1)
        field_label = category._meta.get_field('summary').verbose_name
        assert(field_label == _('Описание'))

    def test_summary_max_length(db, init_db):
        category=Category.objects.get(category_id=1)
        max_length = category._meta.get_field('summary').max_length
        assert(max_length == 500)

    def test_get_absolute_url(db, init_db):
        category=Category.objects.get(category_id=1)
        assert(category.get_absolute_url() == '/catalog/category/1')

class TestItemModel:
    @pytest.fixture
    def init_db(db):
        item_uuid = uuid.uuid4()
        manufactor = Manufactor.objects.create(name='ASUS creator', summary='ASUS summary to be continue')
        category = Category.objects.create(name='VR для домохозяек', summary='Когда-нибудь придумают... наверное...')
        Item.objects.create(item_id=item_uuid, manufactor=manufactor, category=category,
                            name='Когда скучно', summary='Можно включить', price=999.90, quantity=14,
                            availability=False)
        return item_uuid

    def test_name_label(db, init_db):
        item = Item.objects.get(item_id=init_db)
        field_label = item._meta.get_field('name').verbose_name
        assert(field_label == _('Наименование'))

    def test_name_max_length(db, init_db):
        item = Item.objects.get(item_id=init_db)
        max_length = item._meta.get_field('name').max_length
        assert(max_length == 200)

    def test_summary_label(db, init_db):
        item = Item.objects.get(item_id=init_db)
        field_label = item._meta.get_field('summary').verbose_name
        assert(field_label == _('Описание'))

    def test_summary_max_length(db, init_db):
        item = Item.objects.get(item_id=init_db)
        max_length = item._meta.get_field('summary').max_length
        assert(max_length == 500)

    def test_price_decimal_places(db, init_db):
        item = Item.objects.get(item_id=init_db)
        decimal_places = item._meta.get_field('price').decimal_places
        assert(decimal_places == 2)

    def test_get_absolute_url(db, init_db):
        item=Item.objects.get(item_id=init_db)
        assert(item.get_absolute_url() == '/catalog/item/' + str(init_db))
