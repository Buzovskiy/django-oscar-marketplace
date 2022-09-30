from django import template

register = template.Library()


@register.filter(name='check_active')
def check_active(value, arg):
    """
    Function that returns string __active if argument matches value
    """
    return 'tabs__btn--active' if value == arg else ''
