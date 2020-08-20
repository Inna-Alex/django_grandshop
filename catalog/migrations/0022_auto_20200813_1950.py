# Generated by Django 3.0.7 on 2020-08-13 16:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_auto_20200709_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Дата создания категории', verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Дата создания продукта', verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manufactor',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Дата создания производителя', verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Дата создания заказа', verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderitem',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Дата добавления продукта', verbose_name='Дата создания'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='availability',
            field=models.BooleanField(default=False, help_text='Выберите если категория доступна', verbose_name='Доступность'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Введите название категории', max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='summary',
            field=models.CharField(help_text='Введите описание категории', max_length=500, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='item',
            name='availability',
            field=models.BooleanField(default=False, help_text='Выберите если продукт есть в наличии', verbose_name='В наличии'),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='manufactor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Manufactor', verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(help_text='Введите название продукта', max_length=200, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(help_text='Введите количество продукта', verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='item',
            name='summary',
            field=models.CharField(help_text='Введите описание продукта', max_length=500, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='manufactor',
            name='name',
            field=models.CharField(help_text='Введите название производителя', max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='manufactor',
            name='summary',
            field=models.CharField(help_text='Введите описание производителя', max_length=500, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.CharField(help_text='Комментарий к заказу', max_length=500, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('c', 'Создан'), ('p', 'Оплачен'), ('d', 'Доставлен')], default='c', help_text='Статус заказа', max_length=1, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='orderitem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Item', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(help_text='Введите количество продукта', verbose_name='Количество'),
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='catalog_cat_name_39f70b_idx'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['name'], name='catalog_ite_name_9b7e7e_idx'),
        ),
        migrations.AddIndex(
            model_name='manufactor',
            index=models.Index(fields=['name'], name='catalog_man_name_10c8b4_idx'),
        ),
    ]