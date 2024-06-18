from django import template
from django.utils import translation
from oscar_routing.utils import getattr_lang


register = template.Library()


@register.simple_tag
def checkout_order_line_title(order_line):
    translation.activate('ES')
    category = order_line.product.get_categories().first()
    category_name = getattr_lang(category, 'name')
    return f'{category_name} {order_line.upc}'
