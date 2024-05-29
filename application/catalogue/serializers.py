from oscar_routing.utils import site_url, get_lang_lookup, media_site_url
from rest_framework import serializers
from oscar_routing.utils import site_url, get_lang_lookup, getattr_lang

from .models import Product


class ProductChildSerializer(serializers.Serializer):
    request = None
    primary_image = None

    def to_representation(self, instance):
        self.request = self.context.get('request')
        category_obj = instance.get_categories().first()

        # image_not_found
        output = {'productId': instance.id, 'code': instance.upc}

        stock_record = self.request.strategy.select_stockrecord(instance)

        try:
            output['priceInitial'] = float(stock_record.price_initial_1c)
        except (TypeError, AttributeError):
            output['priceInitial'] = 0.0

        try:
            output['discount'] = float(stock_record.price_initial_1c.discount_1c)
        except (TypeError, AttributeError):
            output['discount'] = 0.0

        try:
            # output['price'] = float(self.request.strategy.fetch_for_parent(instance).price.incl_tax)
            output['price'] = round(output['priceInitial'] * (1 - output['discount'] / 100), 2)
        except (TypeError, AttributeError):
            output['price'] = 0.0

        output['currency'] = stock_record.price_currency
        output['shoesType'] = getattr_lang(category_obj, 'slug')
        output['img'] = instance.get_primary_image_or_default_url()
        output['size'] = float(instance.attributes_container.razmer['value'])

        return output


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
