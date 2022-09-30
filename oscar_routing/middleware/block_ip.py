"""
 simple middlware to block IP addresses via settings
 variable BLOCKED_IPS
"""
from django.conf import settings
from django import http


class BlockedIpMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if (request.META['REMOTE_ADDR'] or request.META.get('HTTP_X_REAL_IP')) in settings.BLOCKED_IPS:
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
