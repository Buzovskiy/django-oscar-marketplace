from django.template.loader import render_to_string
from django.http import JsonResponse
from oscar.apps.basket.views import BasketView as BasketViewCore


class BasketView(BasketViewCore):
    def json_response(self, ctx, flash_messages):
        basket_html = render_to_string(
            'oscar/basket/partials/basket_content.html',
            context=ctx, request=self.request)

        mini_basket_html = render_to_string(
            'oscar/partials/mini_basket.html',
            context=ctx, request=self.request)

        return JsonResponse({
            'content_html': basket_html,
            'messages': flash_messages.as_dict(),
            'mini_basket_html': mini_basket_html,
        })

