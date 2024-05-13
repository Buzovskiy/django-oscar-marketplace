# Generated by Django 3.2.7 on 2024-05-08 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0050_filtervalue_productfiltervalue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtervalue',
            name='slug_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Slug EN'),
        ),
        migrations.AlterField(
            model_name='filtervalue',
            name='slug_es',
            field=models.CharField(max_length=255, null=True, verbose_name='Slug ES'),
        ),
        migrations.AlterField(
            model_name='filtervalue',
            name='value_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Value EN'),
        ),
        migrations.AlterField(
            model_name='filtervalue',
            name='value_es',
            field=models.CharField(max_length=255, null=True, verbose_name='Value ES'),
        ),
    ]
