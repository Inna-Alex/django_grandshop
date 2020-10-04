from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manufactor',
            fields=[
                ('manufactor_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Введите название производителя', max_length=200, unique=True, verbose_name='Название')),
                ('summary', models.CharField(blank=True, help_text='Введите описание производителя', max_length=500, null=True, verbose_name='Описание')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Дата создания производителя', verbose_name='Дата создания')),
            ],
            options={
                'db_table': 'gs_manufactor',
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='manufactor',
            index=models.Index(fields=['name'], name='gs_manufact_name_fb0ddf_idx'),
        ),
    ]
