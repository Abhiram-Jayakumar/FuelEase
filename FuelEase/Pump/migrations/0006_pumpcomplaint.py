# Generated by Django 5.0.4 on 2024-05-03 08:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pump', '0005_deliveryboy_license_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='PumpComplaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('admin_reply', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pump', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pump.pump')),
            ],
        ),
    ]