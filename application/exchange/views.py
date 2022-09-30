from django.views.generic import TemplateView
from oscar.core.loading import get_model
import os
from datetime import datetime
from django.conf import settings
from pathlib import Path
import glob
from django.http import HttpResponse
from .files import FileImage, FileXml


class IndexView(TemplateView):
    onec_request = None

    def get(self, request, *args, **kwargs):
        return self.post(request)

    def post(self, request):
        self.onec_request = request

        # http://127.0.0.1:8000/1c_exchange/?mode=checkauth
        if request.GET.get('mode') == 'checkauth':
            return HttpResponse('success\n')

        if request.GET.get('type') == 'catalog' and request.GET.get('mode') == 'init':
            return HttpResponse('zip=no\nfile_limit=10000000\n')  # 10 MB limit

        if request.GET.get('type') == 'clients' and request.GET.get('mode') == 'init':
            return HttpResponse('zip=no\nfile_limit=10000000\n')  # 10 MB limit

        if request.GET.get('type') == 'sale' and request.GET.get('mode') == 'init':
            return HttpResponse('zip=no\nfile_limit=10000000\n')  # 10 MB limit

        if request.GET.get('type') == 'Clients' and request.GET.get('mode') == 'query':
            return HttpResponse('', content_type='text/xml; charset=windows-1251')

        if request.GET.get('type') == 'sale' and request.GET.get('mode') == 'query':
            return HttpResponse('', content_type='text/xml; charset=windows-1251')

        # http://127.0.0.1:8000/1c_exchange/?type=catalog&mode=file&filename=import.xml/
        if request.GET.get('type') == 'catalog' and request.GET.get('mode') == 'file':
            filename = request.GET.get('filename')
            if filename.count('import_files/', 0, 13):  # image
                filename = os.path.basename(filename)
                # remove old file if exists
                FileImage(filename).remove()
                # save image
                FileImage(filename).save_file(self.onec_request.body)
            else:
                filename = os.path.basename(filename)
                # remove old file if exists
                FileXml(filename).remove()
                # save part import.xml
                FileXml().save_part(filename, self.onec_request.body)

            return HttpResponse('success\n')

        if request.GET.get('type') == 'catalog' and request.GET.get('mode') == 'import':
            filename = request.GET.get('filename')
            filename = os.path.basename(filename)  # import.xml
            # merge_files.
            FileXml().make_file(filename)

        return HttpResponse('success\n')
