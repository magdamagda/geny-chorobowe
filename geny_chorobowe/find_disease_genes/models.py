from django.db import models

# Create your models here.

class ClinvarSource(models.Model):
    SourceID = models.IntegerField(primary_key=True)
    SourceName = models.CharField(max_length=50)

class ClinvarGene(models.Model):
    GeneName = models.CharField(max_length=120)
    GeneID = models.IntegerField(primary_key=True)

class ClinvarDisease(models.Model):
	'''wpis o chorobie z bazy clinvar'''
	DiseaseName = models.CharField(max_length=200)
	Source = models.ForeignKey(ClinvarSource, on_delete=models.DO_NOTHING, null=True)
	LastModified = models.DateField()
	ConceptID = models.CharField(max_length=10, primary_key = True)
	DiseaseMIM = models.CharField(max_length=15, null=True, blank=True)
	Genes = models.ManyToManyField(ClinvarGene)

class MedgenConcept(models.Model):
    ConceptID = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=200)
    Def = models.CharField(max_length=10000)
    Source = models.CharField(max_length=50)
    RelatedConcepts = models.ManyToManyField("self", blank=True)