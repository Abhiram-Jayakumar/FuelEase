# Generated by Django 5.0.4 on 2024-04-30 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pump', '0004_deliveryboy_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryboy',
            name='license_number',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]