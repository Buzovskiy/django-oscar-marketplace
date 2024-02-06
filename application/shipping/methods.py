from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static
from oscar.core.loading import get_class


Free = get_class('shipping.methods', 'Free')


class CORREOS(Free):
    code = 'correos-shipping'
    name = 'CORREOS'
    image = static('custom/build/img/shipping/correos.jpg')
    show_name = False


class MRW(Free):
    code = 'mrw-shipping'
    name = 'MRW'
    image = static('custom/build/img/shipping/mrw.png')
    show_name = False


class ConsultationRequired(Free):
    code = 'consultation-required-shipping'
    name = _('Consultation required')
    image = None
    show_name = True
