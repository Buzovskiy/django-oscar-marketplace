from django import template


register = template.Library()


@register.simple_tag
def get_child_products_sizes(child_products):
    sizes = []
    for product in child_products:
        try:
            sizes.append(product.attributes_container.razmer['value'])
        except (AttributeError, KeyError):
            pass
    sizes.sort()
    return sizes


@register.simple_tag
def get_product_size_hyperlink_data(product):
    data = {}
    data['link_class'] = '' if product.is_public else 'product-not-public'
    return data
