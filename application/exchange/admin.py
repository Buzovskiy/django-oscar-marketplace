import mimetypes
import os
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.urls import path
from django.template.response import TemplateResponse
from .admin_form import ExchangeFilesForm
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.core.management import call_command
from .files import FileXml
from .models import Exchange

ExchangeFilesFormSet = formset_factory(ExchangeFilesForm, extra=2)


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        self.request = request
        return Exchange.objects.none()

    def get_urls(self):
        urls = super(ExchangeAdmin, self).get_urls()
        my_urls = [
            # http://127.0.0.1:8000/admin/exchange/exchange/files/
            path('files/', self.exchange_files_list_view, name="exchange-files"),
            path('upload-xml/<path:file_name>', exchange_download_xml_view, name="exchange-download-xml"),
            # http://127.0.0.1:8000/admin/exchange/exchange/haystack-rebuild-index/
            path('haystack-rebuild-index/', exchange_haystack_rebuild_index, name="exchange-haystack-rebuild-index"),
        ]
        return my_urls + urls

    def exchange_files_list_view(self, request):
        if not request.user.is_staff:
            raise PermissionDenied()

        form = ExchangeFilesForm()

        if request.method == 'POST' and request.POST.get('index'):
            form = ExchangeFilesForm(request.POST, request=request)
            form.is_valid()
            return redirect('admin:exchange-files')

        items_count = len(form['image'].field.widget.choices) + len(form['xml'].field.widget.choices)
        context = dict(
            self.admin_site.each_context(request),
            actions_on_top=True,
            action_form=True,  # link jsi18n js file
            form=form,
            items_count=items_count,
        )
        return TemplateResponse(request, 'admin/exchange/files_list.html', context=context)


def exchange_download_xml_view(request, **kwargs):
    file_obj = FileXml(kwargs['file_name'])
    mime_type, _ = mimetypes.guess_type(file_obj.full_path)
    with open(file_obj.full_path, mode='rb') as f:
        content = f.read()
    response = HttpResponse(content, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % os.path.basename(file_obj.file_name)
    return response


def exchange_haystack_rebuild_index(request, **kwargs):
    call_command('rebuild_index', '--noinput')
    return redirect('admin:index')


