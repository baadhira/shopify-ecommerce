# Generated by Django 3.2.12 on 2022-03-21 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0037_alter_orderproduct_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='coupon_used',
        ),
    ]
