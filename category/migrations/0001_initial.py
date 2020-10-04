from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Введите название категории', max_length=200, unique=True, verbose_name='Название')),
                ('summary', models.CharField(blank=True, help_text='Введите описание категории', max_length=500, null=True, verbose_name='Описание')),
                ('availability', models.BooleanField(default=False, help_text='Выберите если категория доступна', verbose_name='Доступность')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Дата создания категории', verbose_name='Дата создания')),
            ],
            options={
                'db_table': 'gs_category',
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='category',
            index=models.Index(fields=['name'], name='gs_category_name_7a364b_idx'),
        ),
    ]
