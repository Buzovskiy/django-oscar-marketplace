from rest_framework.pagination import PageNumberPagination
from rest_framework import status, generics
from rest_framework.decorators import api_view
from django.db.models import Prefetch
from django.http import JsonResponse
from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView
from oscar.core.loading import get_model, get_class
from oscar_routing.utils import site_url, get_lang_lookup

from .serializers import ProductSerializer

ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
Product = get_model('catalogue', 'Product')
get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')


class ProductDetailView(CoreProductDetailView):

    def get_queryset(self):
        qs = super(ProductDetailView, self).get_queryset()
        queryset_attributes = ProductAttributeValue.objects.select_related('attribute').all()
        qs = qs.prefetch_related(
            Prefetch('attributes', queryset=queryset_attributes),
            Prefetch('recommended_products', queryset=Product.objects.browsable().all()),
            Prefetch('recommended_products__attributes', queryset=queryset_attributes),
            Prefetch('children'),
            Prefetch('children__attributes', queryset=queryset_attributes),
            Prefetch('recommended_products__children'),
            Prefetch('recommended_products__children__attributes', queryset=queryset_attributes),
            Prefetch('recommended_products__recommended_products', queryset=Product.objects.browsable().all()),
            Prefetch('recommended_products__recommended_products__attributes', queryset=queryset_attributes),

            Prefetch('parent'),
            Prefetch('parent__attributes', queryset=queryset_attributes),
            Prefetch('parent__recommended_products', queryset=Product.objects.browsable().all()),
            Prefetch('parent__recommended_products__attributes', queryset=queryset_attributes),
            Prefetch('parent__recommended_products__recommended_products', queryset=Product.objects.browsable().all()),
            Prefetch('parent__recommended_products__recommended_products__attributes', queryset=queryset_attributes),
        )

        return qs


class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


@api_view(['GET'])
def get_products_list(request):
    # v1/products/list
    lang_lookup = get_lang_lookup(request)
    # if paginate_by is not set send all products
    paginate_by = request.query_params.get('limit', 100000)
    search_handler = get_product_search_handler_class()(
        request.GET, request.get_full_path(), [], paginate_by=paginate_by)
    search_context = search_handler.get_search_context_data(context_object_name="products")
    data = {
        'items': [],
        'total': int(search_context['paginator'].count),
        'filters': [],
    }
    for item in search_context['products']:
        category_obj = item.get_categories().first()
        category_name = getattr(category_obj, 'name' + lang_lookup, category_obj.name)
        product = {
            'productId': item.id
        }
        primary_image = item.primary_image().original.url if hasattr(item.primary_image(), 'original') else None
        product['img'] = site_url(primary_image) if isinstance(primary_image, str) else None
        product['title'] = f"{category_name} {item.upc}"
        try:
            product['priceInitial'] = float(request.strategy.fetch_for_parent(item).price.price_initial_1c)
        except (TypeError, AttributeError):
            product['priceInitial'] = 0.0

        try:
            product['discountPercent'] = float(request.strategy.fetch_for_parent(item).price.discount_1c)
        except (TypeError, AttributeError):
            product['discountPercent'] = 0.0

        product['discountValue'] = round(product['priceInitial'] * (1 - product['discountPercent'] / 100), 2)

        try:
            product['price'] = float(request.strategy.fetch_for_parent(item).price.incl_tax)
        except (TypeError, AttributeError):
            product['price'] = 0.0

        product['currency'] = request.strategy.fetch_for_parent(item).price.currency

        product['shoesType'] = getattr(category_obj, 'slug' + lang_lookup, category_obj.slug)
        product['productId'] = str(item.id)

        # colors
        product['colorsAvailable'] = []
        product['colorsAvailable'].append({
            'id': 1,
            'image': product['img'],
            'color': item.attributes_container.color_hex_code['value'],
            'productId': str(item.id)
        })
        for item_enum in enumerate(item.recommended_products.all()):
            if hasattr(item_enum[1].primary_image(), 'original'):
                rec_image = item_enum[1].primary_image().original.url
            else:
                rec_image = None
            product['colorsAvailable'].append({
                'id': item_enum[0] + 2,
                'image': rec_image,
                'color': item_enum[1].attributes_container.color_hex_code['value'],
                'productId': str(item_enum[1].id)
            })

        # sizes
        product['sizes'] = []
        sizes = []
        product_children_count = len(item.product_children)
        for item_enum in enumerate(item.product_children):
            try:
                size_value = float(item_enum[1].attributes_container.razmer['value'])
            except (TypeError, AttributeError):
                size_value = 0
            try:
                centimeters = float(item_enum[1].attributes_container.dlina_stelki['value'])
            except (TypeError, AttributeError):
                centimeters = 0
            sizes.append({
                'id': product_children_count - item_enum[0],
                'value': size_value,
                'centimeters': centimeters,
            })
        sizes = sorted(sizes, key=lambda size: size['value'])
        product['sizes'] = sizes

        data['items'].append(product)

    # Filters
    for prod_filter in search_context['facet_data'].items():
        fi_item = {'values': []}
        fi = prod_filter[1]
        fi_item['title'] = fi['name']
        fi_item['category'] = prod_filter[0]

        for fi_value in fi['results']:
            fi_val = {
                'name': fi_value['name'],
                'value': fi_value['name'],
                'count': fi_value['count'],
                'disabled': fi_value['disabled'],
                'selected': fi_value['selected'],
                'show_count': fi_value['show_count'],
            }
            if 'select_url' in fi_value:
                fi_val['select_url'] = fi_value['select_url']
            if 'deselect_url' in fi_value:
                fi_val['deselect_url'] = fi_value['deselect_url']

            fi_item['values'].append(fi_val)

        data['filters'].append(fi_item)

    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
