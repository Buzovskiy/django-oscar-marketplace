# Generated by Django 3.2.7 on 2024-02-29 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0002_add_stripe_api_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appsettings',
            name='key',
            field=models.CharField(max_length=255, unique=True, verbose_name='Key'),
        ),
    ]
