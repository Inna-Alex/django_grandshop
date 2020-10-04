import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Item(models.Model):
    """
    Model representing an item
    """
    item_id = models.UUIDField(primary_key=True,
                               default=uuid.uuid4,
                               verbose_name=_('Идентификатор'))
    manufactor = models.ForeignKey('manufactor.Manufactor',
                                   verbose_name=_('Производитель'),
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    category = models.ForeignKey('category.Category', verbose_name=_('Категория'),
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name=_('Наименование'),
                            help_text="Введите название продукта",
                            unique=True)
    summary = models.CharField(max_length=500, verbose_name=_('Описание'),
                               help_text="Введите описание продукта",
                               null=True, blank=True)
    price = models.DecimalField(max_digits=10, verbose_name=_('Цена'),
                                decimal_places=2,)
    availability = models.BooleanField(verbose_name=_('В наличии'),
                                       default=False,
                                       help_text="Выберите если продукт есть в наличии")
    quantity = models.IntegerField(verbose_name=_('Количество'), default=0,
                                   help_text="Введите количество продукта",)
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'),
                                        help_text="Дата создания продукта")
    last_accessed = models.DateTimeField(verbose_name=_('Дата последнего просмотра'),
                                         null=True, blank=True)
    counter_view = models.BigIntegerField(default=0, verbose_name=_('Количество просмотров'))
    counter_buy = models.BigIntegerField(default=0, verbose_name=_('Количество покупок'))

    def get_absolute_url(self):
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
        db_table = 'gs_item'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
            ]
