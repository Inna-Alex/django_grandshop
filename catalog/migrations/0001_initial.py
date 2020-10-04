from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MailBox',
            fields=[
                ('mail_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Номер письма')),
                ('order_id', models.BigIntegerField(blank=True, null=True, verbose_name='Номер заказа')),
                ('subject', models.CharField(max_length=500, verbose_name='Тема письма')),
                ('body', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Тело письма')),
                ('is_send', models.BooleanField(default=False, verbose_name='Отправлено')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'db_table': 'gs_mailbox',
            },
        ),
    ]
