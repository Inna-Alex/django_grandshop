from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Manufactor(models.Model):
    """
    Model representing an item manufactors
    """
    manufactor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_('Название'),
                            help_text="Введите название производителя",
                            unique=True)
    summary = models.CharField(max_length=500, verbose_name=_('Описание'),
                               help_text="Введите описание производителя",
                               null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'),
                                        help_text="Дата создания производителя")

    def get_absolute_url(self):
        return reverse('manufactor_detail', args=[str(self.manufactor_id)])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'gs_manufactor'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
            ]
