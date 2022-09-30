from django.views.generic import TemplateView
from django.shortcuts import render
from django.db.models import Prefetch
from oscar.core.loading import get_model


Retail = get_model('partner', 'Retail')
RetailAddress = get_model('partner', 'RetailAddress')
RetailCity = get_model('partner', 'RetailCity')
Country = get_model('address', 'Country')


class StoresListView(TemplateView):

    def get(self, request, *args, **kwargs):
        countries = Country.objects.prefetch_related(
            'retailcity_set',
            Prefetch('retailcity_set__retailaddress_set', queryset=RetailAddress.objects.select_related('retail').all())
        ).filter(retailcity__isnull=False).distinct().all()

        addresses = RetailAddress.objects.select_related('retail').all()

        context = {
            'countries': countries,
            'address_objects': addresses,
        }

        return render(request, 'partner/stores.html', context=context)
