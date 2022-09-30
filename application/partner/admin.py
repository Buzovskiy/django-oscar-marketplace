from oscar.apps.partner.admin import *  # noqa
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from oscar.core.loading import get_model
from django.db.models import Count, F

Retail = get_model('partner', 'Retail')
RetailCity = get_model('partner', 'RetailCity')
RetailAddress = get_model('partner', 'RetailAddress')


class RetailAddressInline(admin.StackedInline):
    model = RetailAddress
    extra = 0


class CountriesListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Filter cities by countries')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'country_filter'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        cities = RetailCity.objects.all().values('country').annotate(
            cities_in_country=Count('country'),
            printable_name=F('country__printable_name'),
            country_id=F('country_id')
        )
        lookups = []
        for city in cities:
            lookups.append((city['country_id'], f"{city['printable_name']} ({city['cities_in_country']})"))
        return lookups

    def queryset(self, request, queryset):
        """
        Order of annotation and filter matters
        https://docs.djangoproject.com/en/3.2/topics/db/aggregation/#order-of-annotate-and-filter-clauses
        """
        if self.value():
            queryset = queryset.filter(country=self.value())
        #
        queryset = queryset.annotate(retail_addresses_count=Count('retailaddress'))

        return queryset


@admin.register(RetailCity)
class RetailCityAdmin(admin.ModelAdmin):
    list_display = ['title', 'country', 'retail_addresses_count']
    ordering = ['country']
    inlines = [RetailAddressInline]
    list_filter = (CountriesListFilter,)

    @admin.display(description=_('The number of addresses'))
    def retail_addresses_count(self, obj):
        return obj.retail_addresses_count


@admin.register(Retail)
class RetailAdmin(admin.ModelAdmin):
    inlines = [RetailAddressInline]
    list_display = ('__str__',)
