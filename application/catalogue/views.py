from rest_framework.pagination import PageNumberPagination
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Prefetch
from django.http import JsonResponse, Http404
from oscar.apps.catalogue.views import ProductDetailView as CoreProductDetailView
from oscar.core.loading import get_model, get_class
from oscar_routing.utils import site_url, get_lang_lookup, getattr_lang
from application.catalogue.models import Filter, FilterValue, ProductFilterValue

from .serializers import ProductDetailsSerializer, ProductListSerializer

ProductAttributeValue = get_model('catalogue', 'ProductAttributeValue')
Product = get_model('catalogue', 'Product')
get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')


def product_detail_qs(qs):
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


class ProductDetailView(CoreProductDetailView):

    def get_queryset(self):
        qs = super(ProductDetailView, self).get_queryset()
        return product_detail_qs(qs)


class ProductDetailsAPIView(APIView):
    def get_object(self, pk):
        try:
            qs = product_detail_qs(Product.objects)
            return qs.filter(structure='parent').get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductDetailsSerializer(product, context={'request': request})
        return Response(serializer.data)


class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


@api_view(['GET'])
def get_products_list(request):
    # v1/products/list
    lang_lookup = get_lang_lookup(request)
    # if paginate_by is not set send all products
    paginate_by = request.query_params.get('limit', 100000)

    # Modify query params for Django Haystack
    filters = Filter.objects.prefetch_related('filtervalue_set').all()
    filters_dict = {}
    filters_value_dict = {}
    for f in filters:
        filters_dict[getattr_lang(f, 'slug')] = f.field
        filters_value_dict[f.field] = {'filter_object': f, 'filter_values': {}}
        for fv in f.filtervalue_set.all():
            filters_value_dict[f.field]['filter_values'][getattr_lang(fv, 'slug')] = fv

    new_query_dict = request.GET.copy()
    values_list_modified = []
    for key, value in request.GET.items():
        if key in filters_dict:
            values_list = value.split(',')
            for f_val in values_list:
                values_list_modified.append(f'{filters_dict[key]}_exact:{f_val}')

    new_query_dict.setlist('selected_facets', values_list_modified)

    solr_query_string = ''
    for solr_filter in new_query_dict.getlist('selected_facets', []):
        solr_query_string += f'&selected_facets={solr_filter}'
    # End modify query params

    search_handler = get_product_search_handler_class()(
        new_query_dict, request.get_full_path() + solr_query_string, [], paginate_by=paginate_by)
    search_context = search_handler.get_search_context_data(context_object_name="products")
    data = {
        'items': [],
        'total': int(search_context['paginator'].count),
        'filters': [],
    }

    product_list_serializer = ProductListSerializer(
        search_context['products'], many=True, context={'request': request})

    data['items'] = product_list_serializer.data

    # Filters
    for solr_filter in search_context['facet_data'].items():
        try:
            f_details = filters_value_dict[solr_filter[0]]
        except KeyError:
            continue

        fi_item = {
            'title': getattr_lang(f_details['filter_object'], 'title'),
            'queryKey': getattr_lang(f_details['filter_object'], 'slug'),
            'metadata': {
                'id': f_details['filter_object'].id,
                'key': f_details['filter_object'].slug
            },
            'values': [],
        }

        for solr_filter_value in solr_filter[1]['results']:

            try:
                fv_details = f_details['filter_values'][solr_filter_value['name']]
            except KeyError:
                continue

            fi_item['values'].append({
                'title': getattr_lang(fv_details, 'value'),
                'queryValue': getattr_lang(fv_details, 'slug'),
                'count': solr_filter_value['count'],
                'showCount': solr_filter_value['show_count'],
                'disabled': solr_filter_value['disabled'],
            })

        data['filters'].append(fi_item)

    return JsonResponse(data, status=status.HTTP_200_OK, safe=False)
