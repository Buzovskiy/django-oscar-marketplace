# Generated by Django 3.2.7 on 2022-05-21 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0032_product_external_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='code',
            new_name='external_id',
        ),
    ]
