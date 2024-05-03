from django.utils import translation
from django.conf import settings
from haystack.management.commands import update_index


def decorator_update_backend(f):
    def inner(self, label, using):
        if using in [lang[0] for lang in settings.LANGUAGES]:
            translation.activate(using)
        return f(self, label, using)
    return inner


class Command(update_index.Command):

    @decorator_update_backend
    def update_backend(self, label, using):
        super().update_backend(label, using)
