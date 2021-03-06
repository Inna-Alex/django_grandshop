from django.core.management.sql import emit_post_migrate_signal
from django.db import migrations


def apply_migration(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    emit_post_migrate_signal(2, False, db_alias)
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    managers_group = Group.objects.create(name=u'Managers')
    item_change_perm = Permission.objects.get(name='Can change item')
    item_delete_perm = Permission.objects.get(name='Can delete item')
    managers_group.permissions.add(item_change_perm)
    managers_group.permissions.add(item_delete_perm)


def revert_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model("auth", "Permission")
    Permission.objects.get(name='Can change item').delete()
    Permission.objects.get(name='Can delete item').delete()
    Group.objects.filter(name=u'Managers').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration)
    ]
