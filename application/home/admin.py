from django.contrib import admin
from .models import HomeBanner
from adminsortable2.admin import SortableAdminMixin
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _


@admin.register(HomeBanner)
class HomeBannerAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['__str__', 'image_left_tag', 'image_right_tag']

    @admin.display(description=_('Image left'))
    def image_left_tag(self, obj):
        return mark_safe('<img src="{url}" width="200px" />'.format(url=obj.image_left.url))

    @admin.display(description=_('Image right'))
    def image_right_tag(self, obj):
        return mark_safe('<img src="{url}" width="200px" />'.format(url=obj.image_right.url))
