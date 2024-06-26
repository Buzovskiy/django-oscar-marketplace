# Generated by Django 3.2.7 on 2022-02-15 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0006_auto_20181115_1953'),
        ('partner', '0006_auto_20200724_0909'),
    ]

    operations = [
        migrations.CreateModel(
            name='Retail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the title of retail partner stores', max_length=255, unique=True, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Retail shop partner',
                'verbose_name_plural': 'Retail shop partners',
            },
        ),
        migrations.CreateModel(
            name='RetailAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_description', models.CharField(blank=True, help_text='Enter short description which will be displayed in parenthesis near title or leave field empty', max_length=255, null=True, verbose_name='Short description')),
                ('address', models.CharField(help_text='Enter address of the retail partner store', max_length=255, verbose_name='Address')),
                ('shop_working_hours', models.CharField(blank=True, help_text='Enter store working hours', max_length=255, verbose_name='Store working hours')),
                ('latitude', models.FloatField(blank=True, help_text='Enter latitude coordinate in decimal format, for example 46.43143143569561', null=True, verbose_name='Latitude')),
                ('longitude', models.FloatField(blank=True, help_text='Enter longitude coordinate in decimal format, for example 30.724300888157735', null=True, verbose_name='longitude')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='address.country')),
                ('retail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.retail', verbose_name='Country')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
    ]
