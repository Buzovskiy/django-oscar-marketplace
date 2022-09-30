from django.core.exceptions import ObjectDoesNotExist
from django import forms
from .models import InterviewAttribute, InterviewAttributeValue


class InterviewForm(forms.Form):

    def __init__(self, attr_slug, stage, *args, **kwargs):
        super(InterviewForm, self).__init__(*args, **kwargs)
        interview_choices = []
        try:
            interview_attr = InterviewAttribute.objects.filter(stage=stage).get()
            for attr_value in InterviewAttributeValue.objects.filter(interview_attribute=interview_attr):
                interview_choices.append((attr_value.title, attr_value))
        except ObjectDoesNotExist:
            pass

        self.fields[attr_slug] = forms.ChoiceField(
            widget=forms.RadioSelect, choices=interview_choices, required=False)

        for key in dict(args[0]):
            if not InterviewAttribute.objects.filter(slug=key).count():
                continue
            if key == attr_slug:
                continue
            self.fields[key] = forms.CharField(widget=forms.HiddenInput())
