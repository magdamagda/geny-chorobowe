from urllib2 import urlopen
from datetime import datetime
from django.db import transaction
from .models import ClinvarDisease

def getDiseasesList():
	#na poczatek wywalic wszystkie choroby z bazy
	ClinvarDisease.objects.all().delete()
	#i sciagnac wszystkie od nowa
	req = urlopen('ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/disease_names')
	data = req.read()
	diseases = []
	lines = data.split("\n")
	lines.pop(0)
	with transaction.atomic():
		for line in lines:
			if len(line)>0:
				pola = line.split("\t")
				diseases.append(pola[0])
				lastmod = datetime.strptime(pola[5], '%d %b %Y').strftime('%Y-%m-%d')
				ClinvarDisease.objects.create(DiseaseName=pola[0], SourceName=pola[1], ConceptID=pola[2], \
					SourceID=pola[3], DiseaseMIM=pola[4], LastModified=lastmod, Category=pola[6])

	return diseases

def getDiseasesFromDatabase():
	#przerobic to jakos sensownie
	diseases = ClinvarDisease.objects.filter(Category='Disease')[:20]
	return diseases
