from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from oscar.core.loading import get_class


Free = get_class('shipping.methods', 'Free')


class GLS(Free):
    code = 'gls-shipping'
    name = 'GLS'
    image = static('custom/build/img/shipping/gls.png')
    show_name = False


class DPD(Free):
    code = 'dpd-shipping'
    name = 'DPD'
    image = static('custom/build/img/shipping/dpd.png')
    show_name = False


class ConsultationRequired(Free):
    code = 'consultation-required-shipping'
    name = _('Consultation required')
    image = None
    show_name = True
