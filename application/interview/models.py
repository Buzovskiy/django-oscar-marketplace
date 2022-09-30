from django.db import models
from django.utils.translation import gettext_lazy as _


class InterviewAttribute(models.Model):

    question = models.TextField(null=False, help_text=_('Enter question on the interview page'), default='')
    stage = models.CharField(
        null=False,
        blank=False,
        unique=True,
        max_length=10,
        default='',
        help_text=_("Enter the number of the question which is to be displayed on the interview page, e.g. 01")
    )
    facet_title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        default='',
        help_text=_('Should be the same as key name value in OSCAR_SEARCH_FACETS settings')
    )
    slug = models.SlugField(max_length=255, unique=False, null=True, blank=False, default='')

    objects = models.Manager()

    def __str__(self):
        return f"stage-{self.stage}: {self.facet_title}"

    class Meta:
        verbose_name = _('Filter for the interview')
        verbose_name_plural = _('Filters for the interview')


class InterviewAttributeValue(models.Model):
    interview_attribute = models.ForeignKey(
        InterviewAttribute, on_delete=models.CASCADE)
    title = models.CharField(
        help_text=_('Enter the title of the filter on interview page'), max_length=200, null=False)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=False)
    objects = models.Manager()

    def __str__(self):
        return f"{self.interview_attribute} - {self.title}"

    class Meta:
        verbose_name = _('Filter value for the interview')
        verbose_name_plural = _('Filter values for the interview')


class InterviewAttributeValueRelated(models.Model):
    interview_attribute_value = models.ForeignKey(InterviewAttributeValue, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False)
    objects = models.Manager()

    def __str__(self):
        return self.title
