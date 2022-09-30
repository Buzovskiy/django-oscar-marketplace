import json

from django.views.generic import TemplateView
from django.http import QueryDict
from django.core.paginator import InvalidPage
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from oscar.core.loading import get_class

from .models import InterviewAttribute, InterviewAttributeValueRelated
from .forms import InterviewForm

get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')


class InterviewStart(TemplateView):
    """Start page of the interview"""
    template_name = 'interview/interview-start.html'


class InterviewStage(TemplateView):
    stage_id = None  # comes from url dispatcher
    stage_count = '05'
    attribute_obj = None
    form = None
    get_query_str = ''

    def get(self, request, *args, **kwargs):
        try:
            self.request.GET.__getitem__('submit-05')
            return redirect(mapping_url_with_catalogue_facets(request))
        except KeyError:
            pass
        self.stage_id = kwargs['stage_id']
        self.template_name = f'interview/interview-{self.stage_id}.html'
        copy_of_get_query_dict = request.GET.copy()
        try:
            copy_of_get_query_dict.pop('submit-05')
        except KeyError:
            pass
        self.get_query_str = copy_of_get_query_dict.urlencode()

        try:
            self.attribute_obj = InterviewAttribute.objects.filter(stage=self.stage_id).get()
            self.form = InterviewForm(self.attribute_obj.slug, self.stage_id, request.GET)
        except ObjectDoesNotExist:
            pass
        return super(InterviewStage, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stage_count'] = self.stage_count
        context['attribute_obj'] = self.attribute_obj
        context['form'] = self.form
        context['get_query_str'] = self.get_query_str
        return context


def mapping_url_with_catalogue_facets(request):
    """
    The function for mapping child interview query string with product catalogue query string
    :param request:
    :return: (string) query string parameters + path of filtered catalogue page
    """
    search_handler = get_product_search_handler_class()(QueryDict(), '', [])
    search_context = search_handler.get_search_context_data('products')
    select_urls_list = []
    for facet_key, interview_value in request.GET.items():
        if facet_key not in search_context['facet_data']:
            continue
        related_facets = InterviewAttributeValueRelated.objects.filter(
            interview_attribute_value__title=interview_value,
            interview_attribute_value__interview_attribute__facet_title=facet_key
        )
        related_facets_list = [facet.title.lower() for facet in related_facets]
        for facet in search_context['facet_data'][facet_key]['results']:
            if facet_key.lower() == 'color':
                if json.loads(facet['name'])['color'].lower() in related_facets_list:
                    select_urls_list.append(facet['select_url'].lstrip('?'))
            else:
                if facet['name'].lower() in related_facets_list:
                    select_urls_list.append(facet['select_url'].lstrip('?'))
    query_string = '&'.join(select_urls_list)
    url_for_redirect = reverse('catalogue:index')
    url_for_redirect += '?' + query_string if query_string else ''
    return url_for_redirect
