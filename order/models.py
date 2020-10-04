import uuid
from datetime import date, timedelta

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django_currentuser.db.models import CurrentUserField

from order.signals import order_payed


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
                              choices=ORDER_STATUS, default='c',
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
        db_table = 'gs_order'
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
    orderitem = models.ForeignKey('item.Item', verbose_name=_('Продукт'),
                                  on_delete=models.SET_NULL,
                                  null=True, blank=True)
    quantity = models.IntegerField(verbose_name=_('Количество'),
                                   help_text="Введите количество продукта", default=1)
    price = models.DecimalField(max_digits=10, verbose_name=_('Цена'),
                                decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'),
                                        help_text="Дата добавления продукта")

    def get_absolute_url(self):
        return reverse('orderitem_detail', args=[str(self.order_item_id)])

    def __str__(self):
        return str(self.order_item_id)

    class Meta:
        db_table = 'gs_orderitem'
