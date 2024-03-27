from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings


def check_email_valid(email: str) -> bool:
    """
    The function that checks if email is valid. Returns boolean
    :param email: str
    :return: bool
    """
    try:
        validate_email(email)
    except ValidationError:
        return False
    else:
        return True


def site_url(url: str) -> str:
    return settings.BASE_URL.rstrip('/') + '/' + url.lstrip('/')


def get_lang_lookup(request):
    return '' if settings.LANGUAGE_CODE_1C == request.LANGUAGE_CODE else '_' + request.LANGUAGE_CODE

