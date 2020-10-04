from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('basket_id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(default=1, help_text='Введите количество продукта', verbose_name='Количество')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Дата добавления в корзину', verbose_name='Дата создания')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='item.item', verbose_name='Продукт')),
            ],
            options={
                'db_table': 'gs_basket',
                'ordering': ['created_date'],
            },
        ),
    ]
