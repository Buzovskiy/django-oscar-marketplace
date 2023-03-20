from oscar.apps.payment.admin import *  # noqa
from django.contrib import admin
from .models import PaymentMethod


@admin.register(PaymentMethod)
class PaymentType(admin.ModelAdmin):
    pass
