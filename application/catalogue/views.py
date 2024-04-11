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


# class ApiProductsList(generics.ListAPIView):
#     serializer_class = ProductSerializer
#     pagination_class = ResultsSetPagination
#     queryset = Product.objects.all()
#
#     # def get_queryset(self):
#     #     client_id = self.request.query_params.get('client_id')
#     #     queryset = MessageClient.objects.filter(
#     #         client__client_id=client_id).select_related('client').order_by('-created_at')
#     #     return queryset
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def list(self, request, *args, **kwargs):
#         response = super().list(request, * args, **kwargs)
#         return response

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
        'total': int(search_context['paginator'].count)
    }
    for item in search_context['products']:
        product = {
            'productId': item.id
        }
        primary_image = item.primary_image().original.url if hasattr(item.primary_image(), 'original') else None
        product['img'] = site_url(primary_image) if isinstance(primary_image, str) else None
        product['title'] = item.title
        try:
            product['priceInitial'] = float(request.strategy.fetch_for_parent(item).price.price_initial_1c)
        except TypeError:
            product['priceInitial'] = 0.0

        try:
            product['discountPercent'] = float(request.strategy.fetch_for_parent(item).price.discount_1c)
        except TypeError:
            product['discountPercent'] = 0.0

        product['discountValue'] = round(product['priceInitial'] * (1 - product['discountPercent'] / 100), 2)

        product['price'] = float(request.strategy.fetch_for_parent(item).price.incl_tax)
        product['currency'] = request.strategy.fetch_for_parent(item).price.currency
        shoesType = getattr(item.get_categories().first(), 'name' + lang_lookup)
        if not shoesType:
            shoesType = item.get_categories().first().slug
        product['shoesType'] = shoesType
        product['productId'] = str(item.id)

        # colors
        product['colorsAvailable'] = []
        product['colorsAvailable'].append({
            'id': 0,
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
                'id': item_enum[0] + 1,
                'image': rec_image,
                'color': item_enum[1].attributes_container.color_hex_code['value'],
                'productId': str(item_enum[1].id)
            })

        # sizes
        product['sizes'] = []
        sizes = []
        for item_enum in enumerate(item.product_children):
            sizes.append({
                'id': item_enum[0],
                'value': item_enum[1].attributes_container.size['value'],
            })
        sizes = sorted(sizes, key=lambda size: size['value'])
        product['sizes'] = sizes

        data['items'].append(product)

    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
