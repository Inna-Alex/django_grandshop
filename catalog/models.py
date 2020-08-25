from datetime import date, timedelta
import uuid

from django.db import models
from django.db.models import Transform
from django.db.models.fields import Field, IntegerField
from django.urls import reverse
from django.utils.translation import ngettext_lazy, ugettext_lazy as _

from django_currentuser.db.models import CurrentUserField

ru_time_strings = {
    'year': ngettext_lazy('%d год', '%d лет'),
    'month': ngettext_lazy('%d месяц', '%d месяцев'),
    'week': ngettext_lazy('%d неделя', '%d недели'),
    'day': ngettext_lazy('%d день', '%d дней'),
    'hour': ngettext_lazy('%d час', '%d часов'),
    'minute': ngettext_lazy('%d минута', '%d минут'),
}


class Manufactor(models.Model):
    """
    Model representing an item manufactor
    """
    manufactor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_('Название'),
                            help_text="Введите название производителя")
    summary = models.CharField(max_length=500, verbose_name=_('Описание'),
                               help_text="Введите описание производителя")
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'),
                                        help_text="Дата создания производителя")

    def get_absolute_url(self):
        return reverse('manufactor_detail', args=[str(self.manufactor_id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
            ]


class Category(models.Model):
    """
    Model representing an item category
    """
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_('Название'),
                            help_text="Введите название категории")
    summary = models.CharField(max_length=500, verbose_name=_('Описание'),
                               help_text="Введите описание категории")
    availability = models.BooleanField(default=False,
                                       verbose_name=_('Доступность'),
                                       help_text="Выберите если категория доступна")
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'),
                                        help_text="Дата создания категории")

    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.category_id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
            ]


class Item(models.Model):
    """
    Model representing an item
    """
    item_id = models.UUIDField(primary_key=True,
                               default=uuid.uuid4)
    manufactor = models.ForeignKey('Manufactor',
                                   verbose_name=_('Производитель'),
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    category = models.ForeignKey('Category', verbose_name=_('Категория'),
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name=_('Наименование'),
                            help_text="Введите название продукта")
    summary = models.CharField(max_length=500, verbose_name=_('Описание'),
                               help_text="Введите описание продукта")
    price = models.DecimalField(max_digits=10, verbose_name=_('Цена'),
                                decimal_places=2)
    availability = models.BooleanField(verbose_name=_('В наличии'),
                                       default=False,
                                       help_text="Выберите если продукт есть в наличии")
    quantity = models.IntegerField(verbose_name=_('Количество'),
                                   help_text="Введите количество продукта")
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'),
                                        help_text="Дата создания продукта")
    last_accessed = models.DateTimeField(verbose_name=_('Дата последнего просмотра'),
                                         null=True, blank=True)

    def get_absolute_url(self):
        return reverse('item_detail', args=[str(self.item_id)])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
            ]


class Order(models.Model):
    """
    Model representing an order
    """
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                help_text="Уникальный ID")
    comment = models.CharField(max_length=500, verbose_name=_('Комментарий'),
                               help_text="Комментарий к заказу")
    customer = CurrentUserField()

    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'),
                                        help_text="Дата создания заказа")

    delivery_date = models.DateField(default=date.today() + timedelta(days=5),
                                     verbose_name="Дата доставки",
                                     help_text="Дата доставки заказа")

    ORDER_STATUS = (
        ('c', 'Создан'),
        ('p', 'Оплачен'),
        ('d', 'Доставлен'),
    )

    status = models.CharField(max_length=1, verbose_name=_('Статус'),
                              choices=ORDER_STATUS, blank=True, default='c',
                              help_text='Статус заказа')

    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.order_id)])

    def __str__(self):
        return self.comment

    indexes = [
            models.Index(fields=['created_date'])
            ]


class OrderItem(models.Model):
    """
    Model representing an order item
    """
    order_item_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     help_text="Уникальный ID")
    order = models.ForeignKey('Order', verbose_name=_('Заказ'),
                              on_delete=models.SET_NULL, null=True, blank=True)
    orderitem = models.ForeignKey('Item', verbose_name=_('Продукт'),
                                  on_delete=models.SET_NULL,
                                  null=True, blank=True)
    quantity = models.IntegerField(verbose_name=_('Количество'),
                                   help_text="Введите количество продукта")
    price = models.DecimalField(max_digits=10, verbose_name=_('Цена'),
                                decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'),
                                        help_text="Дата добавления продукта")

    def get_absolute_url(self):
        return reverse('orderitem_detail', args=[str(self.order_item_id)])

    def __str__(self):
        return str(self.order_item_id)


@Field.register_lookup
class NotEqual(models.Lookup):
    lookup_name = 'ne'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params


@IntegerField.register_lookup
class AbsoluteIntValue(Transform):
    lookup_name = 'abs'
    function = 'ABS'
