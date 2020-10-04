from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser


class ItemIssue(models.Model):
    """
    Model representing an item issue from user
    """
    item_issue_id = models.AutoField(primary_key=True)
    item = models.ForeignKey('item.Item', verbose_name=_('Продукт'),
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

    class Meta:
        db_table = 'gs_itemissue'
