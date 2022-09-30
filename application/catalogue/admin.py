from django.contrib import admin
from oscar.apps.catalogue.admin import *  # noqa
from .models import ColorHexCode


@admin.register(ColorHexCode)
class ColorHexCodeAdmin(admin.ModelAdmin):
    list_display = ['color', 'hex_code']
    list_editable = ['hex_code']
    ordering = ('-hex_code',)
