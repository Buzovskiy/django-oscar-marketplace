from django.views.generic import TemplateView


class OnePageCheckoutView(TemplateView):
    template_name = 'oscar/checkout/one_page_checkout.html'