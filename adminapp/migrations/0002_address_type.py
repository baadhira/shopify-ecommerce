# Generated by Django 3.2.12 on 2022-03-13 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
