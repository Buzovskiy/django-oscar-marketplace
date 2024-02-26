import logging
from django.conf import settings


def log_request(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('Middleware called')
        logging.basicConfig(format='%(asctime)s - %(message)s', filename=settings.BASE_DIR / 'logs/app.log')
        logger = logging.getLogger('product_detail_ctx')
        if request.GET.get('logging'):
            logger.warning(f"before view - {request.path}")
        response = get_response(request)
        if request.GET.get('logging'):
            logger.warning(f"after view - {request.path}")
        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware
