from datetime import date, timedelta
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Transform
from django.db.models.fields import Field, IntegerField
from django.urls import reverse
from django.utils.translation import ngettext_lazy, gettext_lazy as _

from django_currentuser.db.models import CurrentUserField

from catalog.signals import order_payed
from users.models import CustomUser

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
                            help_text="Введите название производителя",
                            unique=True)
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
                            help_text="Введите название категории",
                            unique=True)
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
                               default=uuid.uuid4,
                               verbose_name=_('Идентификатор'))
    manufactor = models.ForeignKey('Manufactor',
                                   verbose_name=_('Производитель'),
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    category = models.ForeignKey('Category', verbose_name=_('Категория'),
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name=_('Наименование'),
                            help_text="Введите название продукта",
                            unique=True)
    summary = models.CharField(max_length=500, verbose_name=_('Описание'),
                               help_text="Введите описание продукта")
    price = models.DecimalField(max_digits=10, verbose_name=_('Цена'),
                                decimal_places=2,)
    availability = models.BooleanField(verbose_name=_('В наличии'),
                                       default=False,
                                       help_text="Выберите если продукт есть в наличии")
    quantity = models.IntegerField(verbose_name=_('Количество'),
                                   help_text="Введите количество продукта",)
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'),
                                        help_text="Дата создания продукта")
    last_accessed = models.DateTimeField(verbose_name=_('Дата последнего просмотра'),
                                         null=True, blank=True)
    counter_view = models.BigIntegerField(default=0, verbose_name=_('Количество просмотров'))
    counter_buy = models.BigIntegerField(default=0, verbose_name=_('Количество покупок'))

    def get_absolute_url(self):
        # return reverse('item_detail', args=[str(self.item_id)])
        return reverse('item_counter', args=[str(self.item_id)])

    def update_counter_view(self):
        self.counter_view += 1
        self.save()

    def update_counter_buy(self):
        self.counter_buy += 1
        self.save()

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
    order_id = models.BigAutoField(primary_key=True, help_text="Номер заказа")
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

    def set_status_payed(self):
        self.status = 'p'
        self.save()

    def send_signal_payed(self):
        order_payed.send(sender=self.__class__, order=self, user=self.customer)

    def __str__(self):
        return str(self.order_id).zfill(10)

    class Meta:
        ordering = ['created_date']
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


class Basket(models.Model):
    """
    Model representing user's chosen items
    """
    basket_id = models.AutoField(primary_key=True)
    item = models.ForeignKey('Item', verbose_name=_('Продукт'),
                             on_delete=models.SET_NULL,
                             null=True, blank=True)
    quantity = models.IntegerField(verbose_name=_('Количество'),
                                   help_text="Введите количество продукта",
                                   default=1)
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'),
                                        help_text="Дата добавления в корзину")
    customer = models.ForeignKey(CustomUser, verbose_name=_('Пользователь'),
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)

    class Meta:
        ordering = ['created_date']


class ItemIssue(models.Model):
    """
    Model representing an item issue from user
    """
    item_issue_id = models.AutoField(primary_key=True)
    item = models.ForeignKey('Item', verbose_name=_('Продукт'),
                             on_delete=models.SET_NULL,
                             null=True, blank=True)
    created_by = models.ForeignKey(CustomUser, verbose_name=_('Пользователь'),
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'),
                                        help_text="Дата создания заявки")

    def get_absolute_url(self):
        return reverse('item_issue_detail', args=[str(self.item_issue_id)])

    def __str__(self):
        return str(self.item)


class MailBox(models.Model):
    """
    Model representing an email to be sent to users
    """
    mail_id = models.BigAutoField(primary_key=True, verbose_name="Номер письма")
    order_id = models.BigIntegerField(verbose_name=_('Номер заказа'), null=True, blank=True)
    subject = models.CharField(max_length=500, verbose_name=_('Тема письма'))
    body = models.TextField(max_length=1000, verbose_name=_('Тело письма'))
    customer = models.ForeignKey(CustomUser, verbose_name=_('Клиент'),
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    is_send = models.BooleanField(default=False, verbose_name=_('Отправлено'))
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'))


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
