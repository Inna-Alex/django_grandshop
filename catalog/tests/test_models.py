import uuid

from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from catalog.models import Category, Item, Manufactor


class ManufactorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Manufactor.objects.create(name='ASUS creator',
                                  summary='ASUS summary to be continue')

    def test_name_label(self):
        manufactor = Manufactor.objects.get(manufactor_id=1)
        field_label = manufactor._meta.get_field('name').verbose_name
        self.assertEquals(field_label, _('Название'))

    def test_name_max_length(self):
        manufactor = Manufactor.objects.get(manufactor_id=1)
        max_length = manufactor._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_summary_label(self):
        manufactor = Manufactor.objects.get(manufactor_id=1)
        field_label = manufactor._meta.get_field('summary').verbose_name
        self.assertEquals(field_label, _('Описание'))

    def test_summary_max_length(self):
        manufactor = Manufactor.objects.get(manufactor_id=1)
        max_length = manufactor._meta.get_field('summary').max_length
        self.assertEquals(max_length, 500)

    def test_get_absolute_url(self):
        manufactor = Manufactor.objects.get(manufactor_id=1)
        self.assertEquals(manufactor.get_absolute_url(),
                          '/catalog/manufactor/1')


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='VR для домохозяек',
                                summary='Когда-нибудь придумают...наверное')

    def test_name_label(self):
        category = Category.objects.get(category_id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, _('Название'))

    def test_name_max_length(self):
        category = Category.objects.get(category_id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_summary_label(self):
        category = Category.objects.get(category_id=1)
        field_label = category._meta.get_field('summary').verbose_name
        self.assertEquals(field_label, _('Описание'))

    def test_summary_max_length(self):
        category = Category.objects.get(category_id=1)
        max_length = category._meta.get_field('summary').max_length
        self.assertEquals(max_length, 500)

    def test_get_absolute_url(self):
        category = Category.objects.get(category_id=1)
        self.assertEquals(category.get_absolute_url(), '/catalog/category/1')


class ItemModelTest(TestCase):

    def setUp(self):
        self.item_uuid = uuid.uuid4()
        manufactor = Manufactor.objects.create(name='ASUS creator',
                                               summary='ASUS summary to be continue')
        category = Category.objects.create(name='VR для домохозяек',
                                           summary='Когда-нибудь придумают...наверное')
        Item.objects.create(item_id=self.item_uuid, manufactor=manufactor,
                            category=category, name='Когда скучно',
                            summary='Можно включить', price=999.90,
                            quantity=14, availability=False)

    def test_name_label(self):
        item = Item.objects.get(item_id=self.item_uuid)
        field_label = item._meta.get_field('name').verbose_name
        self.assertEquals(field_label, _('Наименование'))

    def test_name_max_length(self):
        item = Item.objects.get(item_id=self.item_uuid)
        max_length = item._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_summary_label(self):
        item = Item.objects.get(item_id=self.item_uuid)
        field_label = item._meta.get_field('summary').verbose_name
        self.assertEquals(field_label, _('Описание'))

    def test_summary_max_length(self):
        item = Item.objects.get(item_id=self.item_uuid)
        max_length = item._meta.get_field('summary').max_length
        self.assertEquals(max_length, 500)

    def test_price_decimal_places(self):
        item = Item.objects.get(item_id=self.item_uuid)
        decimal_places = item._meta.get_field('price').decimal_places
        self.assertEquals(decimal_places, 2)

    def test_get_absolute_url(self):
        item = Item.objects.get(item_id=self.item_uuid)
        self.assertEquals(item.get_absolute_url(),
                          '/catalog/item/' + str(self.item_uuid))
