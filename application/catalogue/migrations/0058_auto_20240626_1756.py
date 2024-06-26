# Generated by Django 3.2.7 on 2024-06-26 15:56

from django.db import migrations


def forwards_func(apps, schema_editor):
    sorting = apps.get_model('catalogue', 'Sorting')
    sorting.objects.create(field='relevancy', slug='relevancy', slug_en='relevancy', slug_es='relevancia',
                           title_en='relevancy', title_es='relevancia')
    sorting.objects.create(field='newest', slug='newest', slug_en='newest', slug_es='novedades',
                           title_en='newest', title_es='novedades')
    sorting.objects.create(field='price-desc', slug='price-desc', slug_en='price-desc', slug_es='precio-mayor-a-menor',
                           title_en='price descending', title_es='precio mayor a menor')
    sorting.objects.create(field='price-asc', slug='price-asc', slug_en='price-asc', slug_es='precio-menor-a-mayor',
                           title_en='price ascending', title_es='precio menor a mayor')


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0057_sorting'),
    ]

    operations = [migrations.RunPython(forwards_func)]
