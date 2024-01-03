from datetime import datetime
from django import template
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from application.search_optimisation_fields.models import SearchOptimisationFields

register = template.Library()


@register.filter
def meta_title_filter(page_name):
    """
    Get meta title for specific page
    :param page_name: (string) must correspond to desired value of page_name field of SearchOptimisationFields model
    :return: (string) tag title of the page
    """
    try:
        content = SearchOptimisationFields.objects.filter(page_name=page_name).get().meta_title
        if content:
            content += ' | '
    except ObjectDoesNotExist:
        content = ''
    return content


@register.filter
def meta_description_filter(page_name):
    """
    Get meta description for specific page
    :param page_name: (string) must correspond to desired value of page_name field of SearchOptimisationFields model
    :return: (string) meta description of the page
    """
    try:
        content = SearchOptimisationFields.objects.filter(page_name=page_name).get().meta_description
    except ObjectDoesNotExist:
        content = ''
    return content


@register.filter
def meta_keywords_filter(page_name):
    """
    Get meta keywords for specific page
    :param page_name: (string) must correspond to desired value of page_name field of SearchOptimisationFields model
    :return: (string) meta keywords of the page
    """
    try:
        content = SearchOptimisationFields.objects.filter(page_name=page_name).get().meta_keywords
    except ObjectDoesNotExist:
        content = ''
    return content


@register.filter
def static_url_param(value):
    """
    Filter that returns get parameter for static file link.
    Is used in order to get link like app.min.js?v=1667696353.474667 if DEBUG is True or
    app.min.js?v=16 if DEBUG is False where 16 is value
    :param value: value of a parameter
    :return: value of a parameter
    """
    if settings.DEBUG:
        return datetime.timestamp(datetime.now())
    else:
        return value
