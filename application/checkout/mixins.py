import stripe
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from oscar.apps.checkout.mixins import OrderPlacementMixin as OrderPlacementMixinCore
from app_settings.models import AppSettings


class OrderPlacementMixin(OrderPlacementMixinCore):

    def get_message_context(self, order):
        ctx = super().get_message_context(order)
        ctx['client_site_name'] = settings.CLIENT_SITE_NAME
        return ctx

    def handle_redirect_to_payment_page(self, basket):
        next_page_url = self.get_stripe_payment_page_url(basket)
        response = HttpResponseRedirect(next_page_url)
        return response

    def get_stripe_payment_page_url(self, basket):
        stripe.api_key = AppSettings.stripe_api_key.get().value

        line_items = []
        for line in basket.all_lines():
            product = line.product
            try:
                # Trying to get product from stripe
                stripe_product = stripe.Product.retrieve(product.stripe_product_id)
            except stripe.error.InvalidRequestError:
                # If no product in stripe, create it and add to DB
                images = []
                if hasattr(product.primary_image(), 'original') and product.primary_image().original.url:
                    images.append(settings.BASE_URL + product.primary_image().original.url)
                stripe_product = stripe.Product.create(name=product.title.strip(), images=images)
                product.stripe_product_id = stripe_product.id
                product.save()

            # Create price
            price = stripe.Price.create(
                currency=basket.currency.lower(),
                unit_amount=round(float(line.unit_price_incl_tax) * 100),
                product=stripe_product
            )

            line_items.append({
                'price': price,
                'quantity': line.quantity
            })

        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                mode='payment',
                success_url=settings.BASE_URL + reverse('checkout:preview') + "?action=place_order",
                cancel_url=settings.BASE_URL + reverse('checkout:preview')
            )
        except Exception as e:
            return self.get_success_url()

        return checkout_session.url
