# Generated by Django 4.2.15 on 2024-12-23 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_remove_item_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='total',
        ),
    ]
