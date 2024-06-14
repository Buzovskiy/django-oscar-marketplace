from django.conf import settings
from django.utils.functional import SimpleLazyObject, empty
from oscar.apps.basket.middleware import BasketMiddleware as BasketMiddlewareCore


class APIBasketMiddleware(BasketMiddlewareCore):

    def process_response(self, request, response):
        # Delete any surplus cookies
        cookies_to_delete = getattr(request, 'cookies_to_delete', [])
        for cookie_key in cookies_to_delete:
            response.delete_cookie(cookie_key)

        if not hasattr(request, 'basket'):
            return response

        # If the basket was never initialized we can safely return
        if (isinstance(request.basket, SimpleLazyObject)
                and request.basket._wrapped is empty):
            return response

        cookie_key = self.get_cookie_key(request)
        # Check if we need to set a cookie. If the cookies is already available
        # but is set in the cookies_to_delete list then we need to re-set it.
        has_basket_cookie = (
            cookie_key in request.COOKIES
            and cookie_key not in cookies_to_delete)

        # If a basket has had products added to it, but the user is anonymous
        # then we need to assign it to a cookie
        if (request.basket.id and not request.user.is_authenticated
                and not has_basket_cookie):
            cookie = self.get_basket_hash(request.basket.id)
            response.set_cookie(
                cookie_key, cookie,
                max_age=settings.OSCAR_BASKET_COOKIE_LIFETIME,
                secure=settings.OSCAR_BASKET_COOKIE_SECURE,
                samesite='None',  # new
                httponly=True
            )
        return response
