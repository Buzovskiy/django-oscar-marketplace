# Generated by Django 3.2.7 on 2022-05-19 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0030_productattribute_external_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='external_id',
            field=models.CharField(editable=False, max_length=255, null=True, verbose_name='Code in 1c'),
        ),
    ]