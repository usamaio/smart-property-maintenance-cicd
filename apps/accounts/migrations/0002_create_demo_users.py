from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_demo_users(apps, schema_editor):
    User = apps.get_model('accounts', 'User')

    admin_user, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_active': True,
            'is_staff': True,
            'is_superuser': True,
            'role': 'landlord',
        },
    )

    admin_user.email = 'admin@example.com'
    admin_user.is_active = True
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.role = 'landlord'
    admin_user.password = make_password('admin')
    admin_user.save()

    standard_user, _ = User.objects.get_or_create(
        username='user',
        defaults={
            'email': 'user@example.com',
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'role': 'landlord',
        },
    )

    standard_user.email = 'user@example.com'
    standard_user.is_active = True
    standard_user.is_staff = False
    standard_user.is_superuser = False
    standard_user.role = 'landlord'
    standard_user.password = make_password('user')
    standard_user.save()


def remove_demo_users(apps, schema_editor):
    User = apps.get_model('accounts', 'User')

    User.objects.filter(
        username__in=['admin', 'user']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_demo_users,
            remove_demo_users,
        ),
    ]