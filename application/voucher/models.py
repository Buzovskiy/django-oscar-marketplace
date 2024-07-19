from oscar.apps.voucher.abstract_models import AbstractVoucher as AbstractVoucherCore


class Voucher(AbstractVoucherCore):
    def record_usage(self, order, user):
        """
        Records a usage of this voucher in an order.
        """
        if user and user.is_authenticated:
            self.applications.create(voucher=self, order=order, user=user)
        else:
            self.applications.create(voucher=self, order=order)
        self.num_orders += 1
        self.save()
    record_usage.alters_data = True


from oscar.apps.voucher.models import *  # noqa isort:skip