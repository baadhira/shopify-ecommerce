# Generated by Django 3.2.12 on 2022-03-15 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0010_alter_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
