from django import template


register = template.Library()


@register.simple_tag
def get_child_products_sizes(child_products):
    sizes = []
    for product in child_products:
        try:
            sizes.append(product.attributes_container.size['value'])
        except (AttributeError, KeyError):
            pass
    sizes.sort()
    return sizes
