import os
from django import forms
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.utils.translation import gettext_lazy as _
from .files import FileXml, FileImage, get_images_list
from .onec import ImportProduct, ImportOffers, ImportImage, save_filters, populate_color_hex_codes
from application.catalogue.models import update_product_attribute_values_translations
from application.catalogue.models import ProductAttribute


class ExchangeFilesForm(forms.Form):
    """
    Dynamic choices
    https://stackoverflow.com/questions/3419997/creating-a-dynamic-choice-field
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        xml_list = [obj for obj in [FileXml('import.xml'), FileXml('offers.xml')] if obj.full_path.exists()]
        self.fields['xml'].choices = [(obj.file_name, obj) for obj in xml_list]
        self.fields['image'].choices = [(image_obj.file_name, image_obj) for image_obj in get_images_list()]

    xml = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'action-select'},
        ),
        label='',
        choices=[],
    )
    image = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'action-select'},
        ),
        label='',
        choices=[],
    )
    action = forms.ChoiceField(
        label=_('Actions'),
        choices=[
            ('exchange', _('exchange')),
            ('delete', _('delete')),
        ],
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        xml_list = cleaned_data.get("xml")
        image_list = cleaned_data.get("image")

        if xml_list is None:
            raise ValidationError("File import.xml or offers.xml does not exist!")

        for file_name in xml_list:
            if not FileXml(file_name).full_path.exists():
                raise ValidationError(f"File {file_name} does not exist!")
        if not len(xml_list) and not len(image_list):
            raise ValidationError(_('Items must be selected in order to perform actions on them. No items have'))

    def delete_file(self):
        xml_list = self.cleaned_data.get("xml")
        image_list = self.cleaned_data.get("image")
        for file in xml_list:
            FileXml(file).remove()
        for file in image_list:
            FileImage(file).remove()

    def process_data(self):
        xml_list = self.cleaned_data.get("xml")
        image_list = self.cleaned_data.get("image")

        if self.cleaned_data.get("action") == 'delete':
            self.delete_file()
        elif self.cleaned_data.get("action") == 'exchange':
            for xml_file in xml_list:
                if os.path.basename(xml_file) == 'import.xml':
                    save_filters()
                    import_product = ImportProduct(xml_file)
                    import_product.save_product_class()
                    import_product.save_default_partner()
                    import_product.save_categories()
                    import_product.save_attributes()
                    import_product.save_products()
                    import_product.save_recommended()
                    import_product.clean()
                    populate_color_hex_codes()
                    # todo: update product attribute values translations only for products in import.xml
                    update_product_attribute_values_translations(ProductAttribute.objects.all())
                elif os.path.basename(xml_file) == 'offers.xml':
                    import_offers = ImportOffers(xml_file)
                    import_offers.save_stock_records()
                    import_offers.clean()
                    # todo: rebuild index only for products in exchange
                    call_command('rebuild_index', '--noinput')

            for image in image_list:
                import_image_inst = ImportImage(image)
                import_image_inst.save_product_image()
                import_image_inst.clean()
