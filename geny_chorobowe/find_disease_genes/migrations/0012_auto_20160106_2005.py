# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-06 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find_disease_genes', '0011_auto_20160106_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medgenconcept',
            name='Def',
            field=models.CharField(max_length=1000),
        ),
    ]
