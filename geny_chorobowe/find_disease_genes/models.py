from django.db import models

# Create your models here.

class ClinvarDisease(models.Model):
	'''wpis o chorobie z bazy clinvar'''
	#ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/README.txt
	DiseaseName = models.CharField(max_length=120)
	SourceName = models.CharField(max_length=40)
	ConceptID = models.CharField(max_length=10)
	SourceID = models.CharField(max_length=15)
	DiseaseMIM = models.CharField(max_length=15)
	LastModified = models.DateField()
	Category = models.CharField(max_length=25)
	#Blood group,Disease,Finding,Named protein variant,Pharmacological response,phenotype instruction

	def __unicode__(self):
		return self.DiseaseName+' (src: '+self.SourceName+')'
