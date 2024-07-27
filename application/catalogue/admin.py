from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from oscar.apps.catalogue.admin import *  # noqa
from .models import ProductAttribute, Filter, FilterValue, Sorting, \
    update_product_attribute_values_translations, ColorHexCode, AttributeValue, \
    ProductsForExchange

admin.site.unregister(ProductAttribute)


@admin.register(ColorHexCode)
class ColorHexCodeAdmin(admin.ModelAdmin):
    list_display = ['color', 'hex_code']
    list_editable = ['hex_code']
    actions = ['populate_hex_codes']
    ordering = ('-hex_code',)

    @admin.action(description='Populate color hex code to colors filters')
    def populate_hex_codes(self, request, queryset):
        updated_count = 0
        filter_colors_count = FilterValue.objects.filter(filter__field='color').count()
        for source in queryset:
            try:
                color_filter = FilterValue.objects.filter(filter__field='color', value=source.color).get()
                color_filter.hex_code = source.hex_code
                color_filter.save()
                updated_count += 1
            except ObjectDoesNotExist:
                continue
        messages.success(request, f'Updated {updated_count} filter colors of total {filter_colors_count}')


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    readonly_fields = ('external_id',)
    extra = 0


@admin.action(description='Apply translations to product attribute values')
def apply_translations(modeladmin, request, queryset):
    update_product_attribute_values_translations(queryset)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]
    list_display = ('name', 'code', 'product_class', 'type')
    readonly_fields = ('external_id',)
    prepopulated_fields = {"code": ("name",)}
    actions = [apply_translations]


class FilterValueInline(admin.StackedInline):
    model = FilterValue
    readonly_fields = ('value', 'filter')
    extra = 0


@admin.register(Filter)
class FilterAdmin(admin.ModelAdmin):
    inlines = [FilterValueInline]
    list_display = ('field', 'slug', 'slug_en', 'slug_es', 'title_en', 'title_es', 'external_id')
    readonly_fields = ('field',)


@admin.register(Sorting)
class SortingAdmin(admin.ModelAdmin):
    list_display = ('field', 'slug', 'slug_en', 'slug_es', 'title_en', 'title_es', 'default')


@admin.register(ProductsForExchange)
class ProductsForExchangeAdmin(admin.ModelAdmin):
    list_display = ('external_id', 'product')
