import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.BigAutoField(help_text='Номер заказа', primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Дата создания заказа', verbose_name='Дата создания')),
                ('delivery_date', models.DateField(default=datetime.date(2020, 10, 8), help_text='Дата доставки заказа', verbose_name='Дата доставки')),
                ('status', models.CharField(choices=[('c', 'Создан'), ('p', 'Оплачен'), ('d', 'Доставлен')], default='c', help_text='Статус заказа', max_length=1, verbose_name='Статус')),
                ('customer', django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'gs_order',
                'ordering': ['created_date'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('order_item_id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID', primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1, help_text='Введите количество продукта', verbose_name='Количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Дата добавления продукта', verbose_name='Дата создания')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.order', verbose_name='Заказ')),
                ('orderitem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='item.item', verbose_name='Продукт')),
            ],
            options={
                'db_table': 'gs_orderitem',
            },
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['created_date'], name='gs_order_created_379d68_idx'),
        ),
    ]
