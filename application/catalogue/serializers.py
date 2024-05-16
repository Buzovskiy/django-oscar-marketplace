from oscar_routing.utils import site_url, get_lang_lookup
from rest_framework import serializers
from oscar_routing.utils import site_url, get_lang_lookup, getattr_lang

from .models import Product


class ProductSerializer(serializers.Serializer):
    def to_representation(self, instance):
        output = {'images': [], 'color': {}, 'youMayLike': [], 'details': []}

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
            product_data = {'id': recommended_product.id}
            if hasattr(recommended_product.primary_image(), 'original'):
                product_data['image'] = recommended_product.primary_image().original.url
            else:
                product_data['image'] = None

            product_data['shoesType'] = recommended_product.categories.first().slug_es
            output['youMayLike'].append(product_data)

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
