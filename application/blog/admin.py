from django.contrib import admin
from .models import Post
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.html import mark_safe
from adminsortable2.admin import SortableAdminMixin


@admin.register(Post)
class PostAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['id', 'title', 'show_on_website', 'popularity', 'get_popularity_number',
                    'created_on', 'status', 'get_image_preview']
    list_editable = ['status', ]
    list_display_links = ['title']
    list_per_page = 10
    prepopulated_fields = {"slug": ("title",)}

    fields = ['title', 'slug', 'show_on_website', 'image_preview', 'image', 'content', 'status']
    readonly_fields = ('show_on_website',)

    @admin.display(description=_('Image in the list of posts'))
    def get_image_preview(self, obj):
        return obj.admin_image_preview

    @admin.display(description=_(''))
    def get_image_preview(self, obj):
        return obj.admin_image_preview

    @admin.display(description=_('Popularity'))
    def get_popularity_number(self, obj):
        return obj.popularity

    @admin.display(description='id')
    def get_id(self, obj):
        return obj.id

    @admin.display(description=_('Link'))
    def show_on_website(self, obj):
        url = reverse('blog:post-detail', args=(obj.slug,))
        return mark_safe(f'<a title="{_("Show on website")}" href="{url}">{_("Link")}</a>')


