from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class Basket(models.Model):
    """
    Model representing user's chosen items
    """
    basket_id = models.AutoField(primary_key=True)
    item = models.ForeignKey('item.Item', verbose_name=_('Продукт'),
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
        db_table = 'gs_basket'
        ordering = ['created_date']
