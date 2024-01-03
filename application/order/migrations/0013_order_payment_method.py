# Generated by Django 3.2.7 on 2023-03-19 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_paymentmethod'),
        ('order', '0012_shippingaddress_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.paymentmethod', verbose_name='Payment method'),
        ),
    ]