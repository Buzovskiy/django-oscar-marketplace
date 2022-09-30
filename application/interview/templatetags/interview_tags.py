from django import template


register = template.Library()


@register.simple_tag
def get_form_field_choices_list(form, field):
    """
    :param form: form instance
    :param field: the field with the choices
    :return: list of tuples with the choices
    """
    return form[field].field.widget.choices


@register.simple_tag
def print_checked(form, field, value):
    """
    :param form: form instance
    :param field: the field with the choices
    :param value: the value of the field
    :return: string checked if the option is checked
    """
    return 'checked' if form[field].data == value else ''
