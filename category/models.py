from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """
    Model representing an item category
    """
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_('Название'),
                            help_text="Введите название категории",
                            unique=True)
    summary = models.CharField(max_length=500, verbose_name=_('Описание'),
                               help_text="Введите описание категории",
                               null=True, blank=True)
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
        db_table = 'gs_category'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
            ]
