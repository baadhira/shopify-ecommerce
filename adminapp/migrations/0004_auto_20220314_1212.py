# Generated by Django 3.2.12 on 2022-03-14 06:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0003_auto_20220313_1835'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart_item',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cart_item',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Cart_Item',
        ),
    ]
