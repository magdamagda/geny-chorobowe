# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-06 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find_disease_genes', '0009_auto_20160105_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedgenConcept',
            fields=[
                ('ConceptID', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('Name', models.CharField(max_length=200)),
                ('Def', models.CharField(max_length=300)),
                ('Source', models.CharField(max_length=50)),
                ('RelatedConcepts', models.ManyToManyField(blank=True, null=True, related_name='_medgenconcept_RelatedConcepts_+', to='find_disease_genes.MedgenConcept')),
            ],
        ),
        migrations.RenameField(
            model_name='clinvardisease',
            old_name='SourceID',
            new_name='Source',
        ),
        migrations.AlterField(
            model_name='clinvarsource',
            name='SourceName',
            field=models.CharField(max_length=50),
        ),
    ]