# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-05 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find_disease_genes', '0003_auto_20160104_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinvarsource',
            name='SourceID',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
