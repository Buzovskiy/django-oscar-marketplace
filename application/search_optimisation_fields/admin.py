from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import mark_safe
from .models import SearchOptimisationFields


@admin.register(SearchOptimisationFields)
class SearchOptimisationFieldsAdmin(admin.ModelAdmin):
    list_display = ['page_name', 'meta_title', 'meta_description', 'meta_keywords', 'open_page']
    fields = ['page_name', 'meta_title', 'meta_description', 'meta_keywords', 'page_url', 'open_page']
    readonly_fields = ('open_page',)

    @admin.display(description=_('Url of the page'))
    def open_page(self, obj):
        if obj.page_url:
            return mark_safe("<a href='%s'>%s</a>" % (
                obj.page_url,
                obj.page_url
            ))
        else:
            return '-'
