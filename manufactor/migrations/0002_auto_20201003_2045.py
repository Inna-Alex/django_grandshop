from django.db import migrations


def forwards_func(apps, schema_editor):
    Manufactor = apps.get_model('manufactor', 'Manufactor')
    db_alias = schema_editor.connection.alias
    Manufactor.objects.using(db_alias).bulk_create([
        Manufactor(name='ASUS manufactor',
                   summary='Summary for ASUS manufactor'),
        Manufactor(name='Man 1',
                   summary='Summary for Man 1'),
    ])


def reverse_func(apps, schema_editor):
    Manufactor = apps.get_model('manufactor', 'Manufactor')
    db_alias = schema_editor.connection.alias
    Manufactor.objects.using(db_alias).filter(name='ASUS manufactor').delete()
    Manufactor.objects.using(db_alias).filter(name='Man 1').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('manufactor', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
