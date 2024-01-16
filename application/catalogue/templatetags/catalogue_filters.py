import json
from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter(name='show_facet_value')
def show_facet_value(value, field):
    if field == 'color':
        data = json.loads(value)
        return data['color']
    return value


@register.filter(name='is_color_facet')
def is_color_facet(field):
    return field == 'color'


@register.filter(name='get_facet_color_hex_code')
def get_facet_color_hex_code(value):
    data = json.loads(value)
    return data['color_hex_code']


@register.filter(name='get_sort_button_title')
def get_sort_button_title(form):
    """
    The function that excepts form and returns current option title.
    We need it because sort by button may accept different titles according to chosen sorting criteria.
    The default title is sort by.
    :param form: form
    :return: (string) title
    """
    title = _('Sort by')
    for value, option_title in form.fields['sort_by'].choices:
        if value == form['sort_by'].data:
            title = option_title
    return title

