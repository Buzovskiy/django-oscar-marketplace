# Generated by Django 3.2.7 on 2024-05-08 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0048_alter_filter_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='external_id',
            field=models.CharField(help_text='Should be mapped manually to filter field', max_length=255),
        ),
    ]