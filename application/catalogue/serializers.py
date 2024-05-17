from oscar_routing.utils import site_url, get_lang_lookup
from rest_framework import serializers
from oscar_routing.utils import site_url, get_lang_lookup, getattr_lang

from .models import Product


class BaseProductSerializer(serializers.Serializer):
    request = None

    def to_representation(self, instance):
        self.request = self.context.get('request')
        category_obj = instance.get_categories().first()

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

        # sizes
        output['sizes'] = []
        for product_child in instance.children.all():
            try:
                size_value = float(product_child.attributes_container.razmer['value'])
            except (TypeError, AttributeError):
                continue

            try:
                centimeters = float(product_child.attributes_container.dlina_stelki['value'])
            except (TypeError, AttributeError):
                centimeters = 0
            output['sizes'].append({
                'id': product_child.id,
                'value': size_value,
                'centimeters': centimeters,
            })

        output['sizes'] = sorted(output['sizes'], key=lambda size: size['value'])

        return output


class ProductListSerializer(BaseProductSerializer):
    def to_representation(self, instance):
        output = super().to_representation(instance)
        output.update({})
        primary_image = instance.primary_image().original.url if hasattr(instance.primary_image(), 'original') else ''
        output['img'] = site_url(primary_image) if isinstance(primary_image, str) else ''

        # colors
        output['colors'] = []
        output['colors'].append({
            'id': instance.attributes_container.color_hex_code['pav_id'],
            'image': output['img'],
            'value': instance.attributes_container.color_hex_code['value'],
            'productId': instance.id
        })

        for recommended_product in instance.recommended_products.all():
            if hasattr(recommended_product.primary_image(), 'original'):
                rec_image = recommended_product.primary_image().original.url
            else:
                rec_image = None
            output['colors'].append({
                'id': recommended_product.attributes_container.color_hex_code['pav_id'],
                'image': rec_image,
                'value': recommended_product.attributes_container.color_hex_code['value'],
                'productId': recommended_product.id
            })

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
            product_data = {'id': recommended_product.id}
            if hasattr(recommended_product.primary_image(), 'original'):
                product_data['image'] = site_url(recommended_product.primary_image().original.url)
            else:
                product_data['image'] = ''

            product_data['shoesType'] = getattr_lang(recommended_product.categories.first(), 'slug')
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
