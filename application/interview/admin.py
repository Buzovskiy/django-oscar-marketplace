from django.contrib import admin
from .models import InterviewAttribute, InterviewAttributeValue, InterviewAttributeValueRelated


class InterviewAttributeValueRelatedInline(admin.TabularInline):
    model = InterviewAttributeValueRelated
    extra = 0


class InterviewAttributeValueInline(admin.TabularInline):
    model = InterviewAttributeValue
    extra = 0


@admin.register(InterviewAttribute)
class InterviewAttributeAdmin(admin.ModelAdmin):
    inlines = [InterviewAttributeValueInline]
    list_display = ('question', 'stage', 'facet_title', 'slug')
    prepopulated_fields = {'slug': ('facet_title',)}


@admin.register(InterviewAttributeValue)
class InterviewAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'related_facet_values']
    inlines = [InterviewAttributeValueRelatedInline]
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['interview_attribute']

    @admin.display()
    def related_facet_values(self, obj):
        values_list = [_.title for _ in InterviewAttributeValueRelated.objects.filter(interview_attribute_value=obj)]
        return '; '.join(values_list)
