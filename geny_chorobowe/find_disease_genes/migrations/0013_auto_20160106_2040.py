# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-06 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('find_disease_genes', '0012_auto_20160106_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medgenconcept',
            name='Def',
            field=models.CharField(max_length=2000),
        ),
    ]
