# Generated by Django 3.2.7 on 2022-07-18 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InterviewAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the title of the filter on interview page', max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('facet_title', models.CharField(default='', max_length=255)),
            ],
            options={
                'verbose_name': 'Filter for the interview',
                'verbose_name_plural': 'Filters for the interview',
            },
        ),
        migrations.CreateModel(
            name='InterviewAttributeValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter the title of the filter on interview page', max_length=200)),
                ('interview_attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interview.interviewattribute')),
            ],
            options={
                'verbose_name': 'Filter value for the interview',
                'verbose_name_plural': 'Filter values for the interview',
            },
        ),
        migrations.CreateModel(
            name='InterviewAttributeValueRelated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('interview_attribute_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='interview.interviewattributevalue')),
            ],
        ),
    ]