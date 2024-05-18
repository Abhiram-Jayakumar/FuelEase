# Generated by Django 5.0.4 on 2024-04-28 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admintable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_name', models.CharField(max_length=50)),
                ('admin_email', models.EmailField(max_length=254, null=True, unique=True)),
                ('admin_password', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
