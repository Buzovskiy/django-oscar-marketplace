import stripe
from django.http import HttpResponseRedirect
from django.conf import settings
from oscar.apps.checkout.mixins import OrderPlacementMixin as OrderPlacementMixinCore


class OrderPlacementMixin(OrderPlacementMixinCore):

    def handle_successful_order(self, order):
        """
        Handle the various steps required after an order has been successfully
        placed.

        Override this view if you want to perform custom actions when an
        order is submitted.
        """
        # Send confirmation message (normally an email)
        self.send_order_placed_email(order)

        # Flush all session data
        self.checkout_session.flush()

        # Save order id in session so thank-you page can load it
        self.request.session['checkout_order_id'] = order.id

        next_page_url = self.get_stripe_payment_page_url(order)

        response = HttpResponseRedirect(next_page_url)
        self.send_signal(self.request, response, order)
        return response

    def get_stripe_payment_page_url(self, order):
        stripe.api_key = settings.STRIPE_API_KEY

        line_items = []
        for line in order.lines.all():
            product = line.product
            try:
                # Trying to get product from stripe
                stripe_product = stripe.Product.retrieve(product.stripe_product_id)
            except stripe.error.InvalidRequestError:
                # If no product in stripe, create it and add to DB
                images = []
                if product.primary_image().original.url:
                    images.append(settings.BASE_URL + product.primary_image().original.url)
                stripe_product = stripe.Product.create(name=product.title.strip(), images=images)
                product.stripe_product_id = stripe_product.id
                product.save()

            # Create price
            price = stripe.Price.create(
                currency=order.currency.lower(),
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
                success_url=settings.BASE_URL + '/' + self.get_success_url(),
                cancel_url=settings.BASE_URL + '/' + self.get_success_url(),
            )
        except Exception as e:
            return self.get_success_url()

        return checkout_session.url
