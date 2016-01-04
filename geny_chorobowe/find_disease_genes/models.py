from django.db import models

# Create your models here.

class ClinvarSource(models.Model):
    SourceID = models.IntegerField(primary_key=True)
    SourceName = models.CharField(max_length=40)

class ClinvarGene(models.Model):
    GeneName = models.CharField(max_length=120)
    GeneID = models.IntegerField(primary_key=True)

class ClinvarDisease(models.Model):
	'''wpis o chorobie z bazy clinvar'''
	DiseaseName = models.CharField(max_length=120)
	SourceID = models.ForeignKey(ClinvarSource, on_delete=models.DO_NOTHING)
	LastModified = models.DateField()
	ConceptID = models.CharField(max_length=10, null=True, blank=True)
	DiseaseMIM = models.CharField(max_length=15, null=True, blank=True)
	Genes = models.ManyToManyField(ClinvarGene)

	def __unicode__(self):
		return self.DiseaseName+' (src: '+self.SourceName+')'