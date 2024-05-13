from django.conf import settings
from oscar.apps.catalogue.admin import *  # noqa
from .models import ColorHexCode, AttributeValue
from .models import ProductAttribute, Filter, FilterValue

admin.site.unregister(ProductAttribute)


@admin.register(ColorHexCode)
class ColorHexCodeAdmin(admin.ModelAdmin):
    list_display = ['color', 'hex_code']
    list_editable = ['hex_code']
    ordering = ('-hex_code',)


class AttributeValueInline(admin.StackedInline):
    model = AttributeValue
    readonly_fields = ('external_id',)
    extra = 0


@admin.action(description='Apply translations to product attribute values')
def apply_translations(modeladmin, request, queryset):
    qs = queryset.prefetch_related('attributevalue_set')
    for attribute in qs.all():
        for attribute_value in attribute.attributevalue_set.all():
            product_attribute_value = ProductAttributeValue.objects.filter(attribute=attribute)
            product_attribute_value = product_attribute_value.filter(value_external_id=attribute_value.external_id)
            prod_attr_val_data = {}
            for lang in settings.LANGUAGES:
                prod_attr_val_data[f'value_text_{lang[0]}'] = getattr(attribute_value, f'value_{lang[0]}')

            product_attribute_value.update(**prod_attr_val_data)


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


# @admin.register(FilterValue)
# class FilterValueAdmin(admin.ModelAdmin):
#     readonly_fields = ('value', 'filter')
