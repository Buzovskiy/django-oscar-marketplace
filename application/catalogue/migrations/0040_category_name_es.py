# Generated by Django 3.2.7 on 2024-03-27 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0039_product_stripe_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_es',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Name ES'),
        ),
    ]