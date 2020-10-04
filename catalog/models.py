from django.db import models
from django.db.models import Transform
from django.db.models.fields import Field, IntegerField
from django.utils.translation import gettext_lazy as _, ngettext_lazy

from users.models import CustomUser

ru_time_strings = {
    'year': ngettext_lazy('%d год', '%d лет'),
    'month': ngettext_lazy('%d месяц', '%d месяцев'),
    'week': ngettext_lazy('%d неделя', '%d недели'),
    'day': ngettext_lazy('%d день', '%d дней'),
    'hour': ngettext_lazy('%d час', '%d часов'),
    'minute': ngettext_lazy('%d минута', '%d минут'),
}


class MailBox(models.Model):
    """
    Model representing an email to be sent to users
    """
    mail_id = models.BigAutoField(primary_key=True, verbose_name="Номер письма")
    order_id = models.BigIntegerField(verbose_name=_('Номер заказа'), null=True, blank=True)
    subject = models.CharField(max_length=500, verbose_name=_('Тема письма'))
    body = models.TextField(max_length=1000, verbose_name=_('Тело письма'), null=True, blank=True)
    customer = models.ForeignKey(CustomUser, verbose_name=_('Клиент'),
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    is_send = models.BooleanField(default=False, verbose_name=_('Отправлено'))
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('Дата создания'))

    class Meta:
        db_table = 'gs_mailbox'


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
