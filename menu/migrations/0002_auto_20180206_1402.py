# Generated by Django 2.0.2 on 2018-02-06 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.MenuItem'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='tooltip',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]