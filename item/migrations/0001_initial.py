from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        ('manufactor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('name', models.CharField(help_text='Введите название продукта', max_length=200, unique=True, verbose_name='Наименование')),
                ('summary', models.CharField(blank=True, help_text='Введите описание продукта', max_length=500, null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('availability', models.BooleanField(default=False, help_text='Выберите если продукт есть в наличии', verbose_name='В наличии')),
                ('quantity', models.IntegerField(default=0, help_text='Введите количество продукта', verbose_name='Количество')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Дата создания продукта', verbose_name='Дата создания')),
                ('last_accessed', models.DateTimeField(blank=True, null=True, verbose_name='Дата последнего просмотра')),
                ('counter_view', models.BigIntegerField(default=0, verbose_name='Количество просмотров')),
                ('counter_buy', models.BigIntegerField(default=0, verbose_name='Количество покупок')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.category', verbose_name='Категория')),
                ('manufactor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='manufactor.manufactor', verbose_name='Производитель')),
            ],
            options={
                'db_table': 'gs_item',
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['name'], name='gs_item_name_a9bde9_idx'),
        ),
    ]
