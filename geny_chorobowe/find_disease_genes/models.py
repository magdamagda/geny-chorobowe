from django.db import models

# Create your models here.

class ClinvarDisease(models.Model):
	'''wpis o chorobie z bazy clinvar'''
	#ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/README.txt
	DiseaseName = models.CharField(max_length=120)
	SourceName = models.CharField(max_length=40)
	ConceptID = models.CharField(max_length=10, null=True, blank=True)
	SourceID = models.CharField(max_length=15,null=True, blank=True)
	DiseaseMIM = models.CharField(max_length=15, null=True, blank=True)
	LastModified = models.DateField()
	Category = models.CharField(max_length=25)
	#Blood group,Disease,Finding,Named protein variant,Pharmacological response,phenotype instruction

	def __unicode__(self):
		return self.DiseaseName+' (src: '+self.SourceName+')'
