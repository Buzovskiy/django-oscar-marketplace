from django.core.exceptions import ValidationError
from django.core.validators import validate_email


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
