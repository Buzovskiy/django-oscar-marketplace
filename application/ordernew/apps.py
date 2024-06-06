from oscar.core.application import OscarConfig


class OrdernewConfig(OscarConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    label = 'ordernew'
    name = 'application.ordernew'
    namespace = 'ordernew'
