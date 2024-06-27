from oscar_routing.utils import site_url, get_lang_lookup, media_site_url
from rest_framework import serializers
from oscar_routing.utils import site_url, get_lang_lookup, getattr_lang
from django.conf import settings
from .models import Sorting


class SizeSerializer(serializers.Serializer):
    def to_representation(self, instance):
        try:
            size_value = float(instance.attributes_container.razmer['value'])
        except (TypeError, AttributeError):
            size_value = 0

        try:
            centimeters = float(instance.attributes_container.dlina_stelki['value'])
        except (TypeError, AttributeError):
            centimeters = 0
        num_in_stock = instance.stockrecords.filter(partner__name=settings.PARTNER_DEFAULT['name']).first().num_in_stock
        return {
            'id': instance.id,
            'value': size_value,
            'centimeters': centimeters,
            'available': num_in_stock,
        }


class BaseProductSerializer(serializers.Serializer):
    request = None
    primary_image = None

    def to_representation(self, instance):
        self.request = self.context.get('request')
        category_obj = instance.get_categories().first()

        # image_not_found
        output = {'productId': instance.id, 'code': instance.upc}

        try:
            output['priceInitial'] = float(self.request.strategy.fetch_for_parent(instance).price.price_initial_1c)
        except (TypeError, AttributeError):
            output['priceInitial'] = 0.0

        try:
            output['discount'] = float(self.request.strategy.fetch_for_parent(instance).price.discount_1c)
        except (TypeError, AttributeError):
            output['discount'] = 0.0

        try:
            # output['price'] = float(self.request.strategy.fetch_for_parent(instance).price.incl_tax)
            output['price'] = round(output['priceInitial'] * (1 - output['discount'] / 100), 2)
        except (TypeError, AttributeError):
            output['price'] = 0.0

        output['currency'] = self.request.strategy.fetch_for_parent(instance).price.currency

        output['shoesType'] = getattr_lang(category_obj, 'slug')

        self.primary_image = instance.get_primary_image_or_default_url()

        # colors
        output['colors'] = []
        output['colors'].append({
            'id': instance.attributes_container.color_hex_code['pav_id'],
            'image': self.primary_image,
            'value': instance.attributes_container.color_hex_code['value'],
            'productId': instance.id
        })

        for recommended_product in instance.recommended_products.all():
            output['colors'].append({
                'id': recommended_product.attributes_container.color_hex_code['pav_id'],
                'image': recommended_product.get_primary_image_or_default_url(),
                'value': recommended_product.attributes_container.color_hex_code['value'],
                'productId': recommended_product.id
            })

        # sizes
        output['sizes'] = SizeSerializer(instance.children.all(), many=True).data
        output['sizes'] = sorted(output['sizes'], key=lambda size: size['value'])

        return output


class ProductListSerializer(BaseProductSerializer):
    def to_representation(self, instance):
        output = super().to_representation(instance)
        output['img'] = self.primary_image

        return output


class ProductDetailsSerializer(BaseProductSerializer):
    def to_representation(self, instance):
        output = super().to_representation(instance)
        output.update({'images': [], 'color': {}, 'youMayLike': [], 'details': []})

        # images
        for image in instance.get_all_images():
            try:
                image_url = image.original.url
                if not image_url:
                    continue
                output['images'].append(site_url(image_url))
            except (AttributeError, TypeError):
                continue

        # forGender
        try:
            output['forGender'] = instance.attributes_container.pol['value'].lower()
        except (AttributeError, TypeError, KeyError):
            output['forGender'] = None

        try:
            output['color']['id'] = instance.attributes_container.color_hex_code['pav_id']
            output['color']['value'] = instance.attributes_container.color_hex_code['value']
        except (AttributeError, TypeError, KeyError):
            output['color'] = {}

        # youMayLike. Recommended products
        for recommended_product in instance.recommended_products.all():
            output['youMayLike'].append({
                'id': recommended_product.id,
                'image': recommended_product.get_primary_image_or_default_url(),
                'shoesType': getattr_lang(recommended_product.categories.first(), 'slug')
            })

        attribute_codes = ['coloring', 'material_verkha', 'material_vnutrennii', 'khamelion', 'sezon']
        for attribute_code in attribute_codes:
            attribute_data = {}

            # If the product doesn't have attribute, don't write it to the list
            if not hasattr(instance.attributes_container, attribute_code):
                continue

            attribute_container = getattr(instance.attributes_container, attribute_code)
            attribute_data['title'] = getattr_lang(attribute_container['attribute'], 'name')
            attribute_data['description'] = attribute_container['value']
            output['details'].append(attribute_data)

        return output


class ProductBasketLineSerializer(BaseProductSerializer):
    """Serializes child product"""

    def to_representation(self, instance):
        output = super().to_representation(instance.parent)
        output['color'] = {}
        output['img'] = instance.get_primary_image_or_default_url()
        output['size'] = SizeSerializer(instance).data
        try:
            output['color']['id'] = instance.attributes_container.color_hex_code['pav_id']
            output['color']['value'] = instance.attributes_container.color_hex_code['value']
        except (AttributeError, TypeError, KeyError):
            output['color'] = {}

        return output


class OrderingSerializer(serializers.Serializer):
    def to_representation(self, instance):
        output = {
            'title': getattr_lang(instance, 'title'),
            'queryKey': getattr_lang(instance, 'slug'),
            'values': []
        }

        active_sorting_field = self.context.get('active_sorting_field')
        for sorting_method in Sorting.objects.all():
            output['values'].append({
                'id': sorting_method.id,
                'title': getattr_lang(sorting_method, 'title'),
                'queryValue': getattr_lang(sorting_method, 'slug'),
                'active': True if active_sorting_field == sorting_method.field else False
            })

        return output
