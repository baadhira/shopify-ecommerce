# Generated by Django 3.2.12 on 2022-03-14 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0008_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_item',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
