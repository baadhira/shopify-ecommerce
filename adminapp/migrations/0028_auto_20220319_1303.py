# Generated by Django 3.2.12 on 2022-03-19 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0027_orderproduct_coupon_used'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='couponused',
            name='coupon',
        ),
        migrations.RemoveField(
            model_name='couponused',
            name='order',
        ),
        migrations.RemoveField(
            model_name='couponused',
            name='user',
        ),
        migrations.DeleteModel(
            name='Coupon',
        ),
        migrations.DeleteModel(
            name='Couponused',
        ),
    ]
