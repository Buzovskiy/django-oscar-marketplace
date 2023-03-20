from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from oscar.core.loading import get_model
from oscar.apps.order.utils import OrderDispatcher as OrderDispatcherCore

CommunicationEventType = get_model('communication', 'CommunicationEventType')


class OrderDispatcher(OrderDispatcherCore):

    def dispatch_order_messages(self, order, messages, event_code, attachments=None, **kwargs):
        """
        Dispatch order-related messages to the customer.
        """
        self.dispatcher.logger.info("Order #%s - sending %s messages", order.number, event_code)
        if order.is_anonymous:
            email = kwargs.get('email_address', order.guest_email)
            dispatched_messages = self.dispatcher.dispatch_anonymous_messages(email, messages, attachments)
        else:
            user = order.user
            # Try taking email from shipping address. If fail use user's email.
            try:
                email = order.shipping_address.email
                validate_email(email)
            except ValidationError:
                email = user.email
            user.email = email
            dispatched_messages = self.dispatcher.dispatch_user_messages(user, messages, attachments)

        try:
            event_type = CommunicationEventType.objects.get(code=event_code)
        except CommunicationEventType.DoesNotExist:
            event_type = None

        self.create_communication_event(order, event_type, dispatched_messages)

