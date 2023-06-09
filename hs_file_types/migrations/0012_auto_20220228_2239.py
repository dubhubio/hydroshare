# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-02-28 22:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import hs_core.hs_rdf


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('hs_file_types', '0011_auto_20201212_1554'),
    ]

    operations = [
            migrations.CreateModel(
                name='OriginalCoverage',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('object_id', models.PositiveIntegerField()),
                    ('_value', models.CharField(max_length=1024, null=True)),
                    ('projection_string_type', models.CharField(choices=[('', '---------'), ('WKT String', 'WKT String'), ('Proj4 String', 'Proj4 String')], max_length=20, null=True)),
                    ('projection_string_text', models.TextField(blank=True, null=True)),
                    ('datum', models.CharField(blank=True, max_length=300)),
                    ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hs_file_types_originalcoverage_related', to='contenttypes.ContentType')),
                ],
                bases=(models.Model, hs_core.hs_rdf.RDF_Term_MixIn),
            ),
            migrations.CreateModel(
                name='Variable',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('object_id', models.PositiveIntegerField()),
                    ('name', models.CharField(max_length=1000)),
                    ('unit', models.CharField(max_length=1000)),
                    ('type', models.CharField(choices=[('Char', 'Char'), ('Byte', 'Byte'), ('Short', 'Short'), ('Int', 'Int'), ('Float', 'Float'), ('Double', 'Double'), ('Int64', 'Int64'), ('Unsigned Byte', 'Unsigned Byte'), ('Unsigned Short', 'Unsigned Short'), ('Unsigned Int', 'Unsigned Int'), ('Unsigned Int64', 'Unsigned Int64'), ('String', 'String'), ('User Defined Type', 'User Defined Type'), ('Unknown', 'Unknown')], max_length=1000)),
                    ('shape', models.CharField(max_length=1000)),
                    ('descriptive_name', models.CharField(blank=True, max_length=1000, null=True, verbose_name='long name')),
                    ('method', models.TextField(blank=True, null=True, verbose_name='comment')),
                    ('missing_value', models.CharField(blank=True, max_length=1000, null=True)),
                    ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hs_file_types_variable_related', to='contenttypes.ContentType')),
                ],
                options={
                    'abstract': False,
                },
                bases=(models.Model, hs_core.hs_rdf.RDF_Term_MixIn),
            ),
            migrations.AlterUniqueTogether(
                name='originalcoverage',
                unique_together=set([('content_type', 'object_id')]),
            ),
        ]

