from django.conf import settings
from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_or_update_admin_user(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split('.')
    User = apps.get_model(app_label, model_name)

    username = 'admin'
    password = 'admin'

    try:
        user = User.objects.get(username=username)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.password = make_password(password)
        user.save()
    except User.DoesNotExist:
        create_kwargs = {
            'username': username,
            'is_superuser': True,
            'is_staff': True,
            'is_active': True,
            'password': make_password(password),
        }
        if 'email' in {f.name for f in User._meta.get_fields()}:
            create_kwargs.setdefault('email', 'admin@example.com')
        User.objects.create(**create_kwargs)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('rpgdice', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(create_or_update_admin_user, noop),
    ]
