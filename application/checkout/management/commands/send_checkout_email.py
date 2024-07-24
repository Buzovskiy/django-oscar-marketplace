import stripe
from django.template.loader import render_to_string
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from oscar.core.loading import get_class, get_model
from application.catalogue.models import Product

Order = get_model('order', 'Order')


class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mail(
            "Subject here",
            "Here is the message.",
            "no-reply@weestep.es",
            [""],
            fail_silently=False,
        )
