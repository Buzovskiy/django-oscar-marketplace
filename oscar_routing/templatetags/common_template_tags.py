from django import template
from django.urls import translate_url as django_translate_url
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_pagination_numbers(page_obj, on_each_side=1, on_ends=1, **kwargs):
    return page_obj.paginator.get_elided_page_range(number=page_obj.number,
                                                    on_each_side=on_each_side,
                                                    on_ends=on_ends)


@register.filter()
def is_number(value):
    """
    Проверяем является ли переменная int
    :param value:
    :return: bool
    """
    return type(value) == int


@register.simple_tag(takes_context=True)
def translate_url(context, lang_code):
    path = context.get('request').get_full_path()
    return django_translate_url(path, lang_code)
