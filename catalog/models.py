from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField
from django.utils.translation import ugettext_lazy as _
import uuid

class Manufactor(models.Model):
    """
    Model representing an item manufactor
    """
    manufactor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_('Название'), help_text="Введите название производителя")
    summary = models.CharField(max_length=500, verbose_name=_('Описание'), help_text="Введите описание производителя")

    def get_absolute_url(self):
        return reverse('manufactor_detail', args=[str(self.manufactor_id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Category(models.Model):
    """
    Model representing an item category
    """
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_('Название'), help_text="Введите название категории")
    summary = models.CharField(max_length=500, verbose_name=_('Описание'), help_text="Введите описание категории")
    availability = models.BooleanField(default=False, verbose_name=_('Доступность'), help_text="Выберите если категория доступна")

    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.category_id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Item(models.Model):
    """
    Model representing an item
    """
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    manufactor = models.ForeignKey('Manufactor', verbose_name=_('Производитель'), on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey('Category', verbose_name=_('Категория'), on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name=_('Наименование'), help_text="Введите название продукта")
    summary = models.CharField(max_length=500, verbose_name=_('Описание'), help_text="Введите описание продукта")
    price = models.DecimalField(max_digits=10, verbose_name=_('Цена'), decimal_places=2)
    availability = models.BooleanField(verbose_name=_('В наличии'), default=False, help_text="Выберите если продукт есть в наличии")
    quantity = models.IntegerField(verbose_name=_('Количество'), help_text="Введите количество продукта")

    def get_absolute_url(self):
        return reverse('item_detail', args=[str(self.item_id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
    
class Order(models.Model):
    """
    Model representing an order
    """
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID")
    comment = models.CharField(max_length=500, verbose_name=_('Комментарий'), help_text="Комментарий к заказу")
    customer = CurrentUserField()

    ORDER_STATUS = (
        ('c', 'Создан'),
        ('p', 'Оплачен'),
        ('d', 'Доставлен'),
    )
    
    status = models.CharField(max_length=1, verbose_name=_('Статус'), choices=ORDER_STATUS, blank=True, default='c', help_text='Статус заказа')

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.order_id)])

    def __str__(self):
        return self.comment

    #class Meta:
        #ordering = ['name']

class OrderItem(models.Model):
    """
    Model representing an order item
    """
    order_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный ID")
    order = models.ForeignKey('Order', verbose_name=_('Заказ'), on_delete=models.SET_NULL, null=True, blank=True)
    orderitem = models.ForeignKey('Item', verbose_name=_('Продукт'), on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(verbose_name=_('Количество'), help_text="Введите количество продукта")
    price = models.DecimalField(max_digits=10, verbose_name=_('Цена'), decimal_places=2)

    def get_absolute_url(self):
        return reverse('orderitem_detail', args=[str(self.order_item_id)])

    def __str__(self):
        return str(self.order_item_id)

    #class Meta:
        #ordering = ['name']

