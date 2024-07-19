from asgiref.sync import async_to_sync
import stripe
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from telegram import Bot
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

    def send_order_placed_telegram_notification(self, order):
        data_voucher = order.data_for_voucher_notification
        text = "*Новый заказ!*\n"
        text += f"\nid заказа: *{order.id}*; \n\n"
        for line in order.lines.all():
            text += f"{line.title} x {line.quantity} - *{line.line_price_incl_tax}{order.currency}* \n"
        text += f"\nBasket total: *{order.basket_total_incl_tax}{order.currency}*"
        text += f"\nShipping: *{order.shipping_incl_tax}{order.currency}*"
        text += f"\nOrder total: *{order.total_incl_tax}{order.currency}*"
        if data_voucher:
            text += f"\n{data_voucher[0]}: *{data_voucher[1]}*"
        text += f"\n\nShipping method: *{order.shipping_method}*"
        text += f"\nClient data:"
        # for field in order.shipping_address.active_address_fields():
        #     text += f"\n*{field}*"
        for key, value in order.shipping_address.get_data_for_notification().items():
            text += f"\n{key}: *{value}*"

        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        async_to_sync(bot.send_message)(
            chat_id=settings.TELEGRAM_GROUP_CHAT_ID,
            text=text,
            parse_mode='markdown'
        )
