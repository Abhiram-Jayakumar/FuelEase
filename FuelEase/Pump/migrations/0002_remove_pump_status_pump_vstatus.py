# Generated by Django 5.0.4 on 2024-04-28 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pump', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pump',
            name='status',
        ),
        migrations.AddField(
            model_name='pump',
            name='vstatus',
            field=models.IntegerField(default=0),
        ),
    ]
