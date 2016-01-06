# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-04 21:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('find_disease_genes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClinvarDisease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DiseaseName', models.CharField(max_length=120)),
                ('LastModified', models.DateField()),
                ('ConceptID', models.CharField(blank=True, max_length=10, null=True)),
                ('DiseaseMIM', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClinvarGene',
            fields=[
                ('GeneName', models.CharField(max_length=120)),
                ('GeneID', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='ClinvarSource',
            fields=[
                ('SourceID', models.IntegerField(primary_key=True, serialize=False)),
                ('SourceName', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='GeneDisease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DiseaseID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='find_disease_genes.ClinvarDisease')),
                ('GeneID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='find_disease_genes.ClinvarGene')),
            ],
        ),
        migrations.DeleteModel(
            name='Disease',
        ),
        migrations.DeleteModel(
            name='Gene',
        ),
        migrations.AddField(
            model_name='clinvardisease',
            name='SourceID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='find_disease_genes.ClinvarSource'),
        ),
    ]
