# Generated by Django 3.2.7 on 2023-03-13 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20200801_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
