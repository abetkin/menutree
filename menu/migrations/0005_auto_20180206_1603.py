# Generated by Django 2.0.2 on 2018-02-06 16:03

from django.db import migrations
from django.conf import settings

from django.contrib.auth.models import User

def create_admin(apps, se):
    if not settings.DEBUG:
        return
    admin = User(username='admin', is_staff=True, is_superuser=True)
    admin.set_password('admin')
    admin.save()

class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_auto_20180206_1552'),
    ]

    operations = [
        migrations.RunPython(create_admin)
    ]
