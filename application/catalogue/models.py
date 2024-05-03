from django.core.exceptions import ValidationError
from oscar.core.utils import slugify
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.conf import settings
from oscar.apps.catalogue.abstract_models import \
    AbstractProduct, \
    AbstractCategory, \
    AbstractProductAttribute, \
    AbstractProductAttributeValue
from .utils import validate_sizes
from oscar_routing.utils import getattr_lang
from .product_attributes import PrefetchedProductAttributesContainer


class ProductAttributeValue(AbstractProductAttributeValue):

    value_text_en = models.TextField(_('Text EN'), blank=True, null=True)
    value_text_es = models.TextField(_('Text ES'), blank=True, null=True)
    value_external_id = models.CharField(_('Value external ID'), max_length=255, blank=True, null=True)

    @property
    def value_text_lang(self):
        """Get value_text taking into account active language"""
        return getattr_lang(self, 'value_text')

    def save(self, *args, **kwargs):
        self.clean()
        return super(ProductAttributeValue, self).save(*args, **kwargs)

    def clean(self):
        if (self.attribute.code == settings.ATTR_SIZES_CODE and
                self.product.get_product_class().slug == settings.PRODUCT_CLASS_SHOES_SLUG):
            if self.value_text is not None and not validate_sizes(self.value_text):
                raise ValidationError(
                    _("Sizes must by like: 20-26"))


class Product(AbstractProduct):

    external_id = models.CharField(
        _('Code in 1c'), max_length=255, editable=False, null=True, unique=True
    )

    stripe_product_id = models.CharField(max_length=255, null=True, blank=True)

    @property
    def attributes_container(self):
        """
        Property that makes possible to call product attribute in this way:
        product.attributes_container.color_code['value']
        """
        return PrefetchedProductAttributesContainer(self)

    def custom_save(self, *args, **kwargs):
        """
        Method that saves only product,
        not attributes like method save() in AbstractProduct
        """
        if not self.slug:
            self.slug = slugify(self.get_title())
        super(AbstractProduct, self).save(*args, **kwargs)

    @property
    def children_ordered_by_size(self):
        """
        Getter that returns the list of products sorted by size
        :return: list
        """
        children = list(self.children.all())
        try:
            children.sort(key=lambda el: el.attributes_container.razmer['value'], reverse=False)
        except AttributeError as e:
            pass
        return children

    @property
    def category_first(self):
        """Getter that returns product category"""
        if self.is_child:
            return self.parent.categories.first()
        else:
            return self.categories.first()

    def get_parent(self):
        """Get parent of a product"""
        if self.is_child:
            return self.parent
        else:
            return self


class Category(AbstractCategory):

    external_id = models.CharField(
        _('Code in 1c'), max_length=255, editable=False, null=True, unique=True)

    product_description = models.TextField(
        _('Product description'),
        blank=True,
        null=True,
        help_text=_('Enter product description that is to display on product page')
    )
    product_long_description = models.TextField(
        _('Product long description'),
        blank=True,
        null=True,
        help_text=_('Enter product long description that is to display on product page')
    )
    product_design_description = models.TextField(
        _('Product design description'),
        blank=True,
        null=True,
        help_text=_('Enter product design description that is to display on product page')
    )
    product_benefits_description = models.TextField(
        _('Product benefits description'),
        blank=True,
        null=True,
        help_text=_('Enter product benefits description that is to display on product page')
    )

    name_es = models.CharField(_('Name ES'), max_length=255, null=True, blank=True)
    name_en = models.CharField(_('Name EN'), max_length=255, null=True, blank=True)
    slug_es = models.CharField(_('Slug ES'), max_length=255, null=True, blank=True)

    @property
    def full_name(self):
        """
        Returns a string representation of the category and it's ancestors,
        e.g. 'Books > Non-fiction > Essential programming'.

        It's rarely used in Oscar, but used to be stored as a CharField and is
        hence kept for backwards compatibility. It's also sufficiently useful
        to keep around.
        """
        names = [getattr_lang(category, 'name') for category in self.get_ancestors_and_self()]
        return self._full_name_separator.join(names)


class ProductAttribute(AbstractProductAttribute):

    external_id = models.CharField(
        _('Code in 1c'), max_length=255, editable=False, null=True, unique=False
    )


class AttributeValue(models.Model):
    attribute = models.ForeignKey('catalogue.ProductAttribute', on_delete=models.CASCADE)
    external_id = models.CharField(max_length=255, editable=False, null=False, blank=False)
    value = models.CharField(max_length=255, blank=True, null=True)
    value_es = models.CharField(_('Value ES'), max_length=255, blank=True, null=True)
    value_en = models.CharField(_('Value EN'), max_length=255, blank=True, null=True)

    def __str__(self):
        return self.value


class ColorHexCode(models.Model):
    color = models.CharField(
        _('Color name'),
        max_length=255,
        unique=True,
        help_text=_('Color name, e.g. black '),
    )
    hex_code = models.CharField(
        _('Hex code'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('Color hex code, e.g. #000000')
    )

    def __str__(self):
        parts = [self.color, self.hex_code]
        return " - ".join([str(el) for el in parts if el])

    class Meta:
        verbose_name = _('Color hex code')


from oscar.apps.catalogue.models import *  # noqa isort:skip


@receiver(m2m_changed, sender=Product.categories.through)
def product_category_changed(sender, instance, action, model, pk_set, **kwargs):
    if action == "post_add" and not instance.title:
        category = model.objects.get(pk=list(pk_set).pop())
        instance.title = f"Kids {category.name} {instance.upc}"
        instance.save()
