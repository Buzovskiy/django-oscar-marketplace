from django import template

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
