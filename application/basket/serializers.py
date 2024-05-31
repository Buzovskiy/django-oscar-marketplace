from django.db.models import Prefetch
from rest_framework import serializers
from .models import Basket, Line
from application.catalogue.serializers import ProductBasketLineSerializer
from application.catalogue.models import Product
from oscar.core.loading import get_model, get_class
ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')


class BasketLineSerializer(serializers.Serializer):
    def to_representation(self, instance):
        qs = Product.objects.filter(pk=instance.product.pk)

        queryset_attributes = ProductAttributeValue.objects.select_related('attribute').all()
        qs = qs.prefetch_related(
            Prefetch('attributes', queryset=queryset_attributes),
            Prefetch('parent'),
            Prefetch('parent__attributes', queryset=queryset_attributes),
        )

        output = {
            'id': instance.id,
            'quantity': instance.quantity,
            'itemsTotal': instance.line_price_incl_tax,
            'product': ProductBasketLineSerializer(qs.get(), context={'request': self.context['request']}).data
        }
        return output


class BasketCheckParamsSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    sizeId = serializers.IntegerField()


class BasketSerializer(serializers.Serializer):

    def to_representation(self, instance):
        items = BasketLineSerializer(instance.all_lines(), many=True, context={'request': self.context['request']})
        output = {
            'id': instance.id,
            'total': instance.total_incl_tax,
            'numItems': instance.num_items,
            'items': items.data,
        }
        return output


class BasketLinePatchSerializer(serializers.Serializer):
    sizeId = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def create(self, validated_data):
        product = validated_data['product']
        stock_record = validated_data['stock_record']
        line_reference = f"{product.id}_{stock_record.id}"
        return Line.objects.create(
            basket=validated_data['basket'],
            line_reference=line_reference,
            product=product,
            stockrecord=stock_record,
            quantity=validated_data['quantity'],
            price_currency=stock_record.price_currency,
            price_excl_tax=stock_record.price,
            price_incl_tax=stock_record.price
        )

    def update(self, instance, validated_data):
        product = validated_data['product']
        stock_record = validated_data['stock_record']
        line_reference = f"{product.id}_{stock_record.id}"

        instance.basket = validated_data['basket']
        instance.line_reference = line_reference
        instance.product = product
        instance.stockrecord = stock_record
        instance.quantity = validated_data['quantity']
        instance.price_currency = stock_record.price_currency
        instance.price_excl_tax = stock_record.price
        instance.price_incl_tax = stock_record.price
        instance.save()
        return instance
