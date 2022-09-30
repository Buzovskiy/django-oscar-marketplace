from django.views.generic.edit import FormView
from .forms import ContactsForm
from django.urls import reverse_lazy


class ContactsView(FormView):
    template_name = 'contacts/contacts-view.html'
    form_class = ContactsForm

    def get_success_url(self):
        return reverse_lazy('contacts:contacts') + '?message=success'

    def get_context_data(self, **kwargs):
        context = super(ContactsView, self).get_context_data(**kwargs)
        if 'message' in context['view'].request.GET and context['view'].request.GET['message'] == 'success':
            context['message'] = 'success'
        else:
            context['message'] = ''
        return context

    def form_valid(self, form):
        form.send_email(request=self.request)
        return super().form_valid(form)


class BecomeOurPartnerView(ContactsView):
    template_name = 'contacts/become-our-partner.html'

    def get_success_url(self):
        return reverse_lazy('contacts:become-our-partner') + '?message=success'
