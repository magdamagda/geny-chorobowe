from urllib2 import urlopen
from datetime import datetime
from django.db import transaction
from .models import ClinvarDisease

sourcePath = "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/gene_condition_source_id"

def updateDiseasesList():
	#na poczatek wywalic wszystkie choroby z bazy
	ClinvarDisease.objects.all().delete()
	#i sciagnac wszystkie od nowa
	req = urlopen(sourcePath)
	data = req.read()
	diseases = set()
	genesDict = {}
	genes = set()
	sources = set()
	lines = data.split("\n")
	lines.pop(0)
	for line in lines:
		if len(line)>0:
			pola = line.split("\t")
			lastmod = datetime.strptime(pola[7], '%d %b %Y').strftime('%Y-%m-%d')
			concept = pola[2]
			diseases.add([concept, pola[3], pola[5], pola[6], lastmod]) #concept, name, sourceID, mim, last_mod
			if not concept in genesDict:
				genesDict[concept] = []
			genesDict[concept].append(pola[0])
			genes.add([pola[0], pola[1]]) #id, name
			sources.add([pola[5], pola[4]]) #id, name
	#insert genes
	with transaction.atomic():
		for gene in genes:
			ClinvarGene.objects.create(GeneName = gene[1] , GeneID = gene[0])

	#insert sources
	with transaction.atomic():
		for s in sources:
			ClinvarSource.objects.create(SourceName = s[1] , SourceID = s[0])
			
	#insert diseases
	with transaction.atomic():
		for d in diseases:
			disease = ClinvarDisease(DiseaseName = d[1], SourceID = d[2], LastModified = d[4], ConceptID=d[0], DiseaseMIM = d[3] )
			disease.Genes.add(ClinvarGene.objects.get(GeneID = genesDict[d[0]]))

def getDiseasesFromDatabase(name=None, gene=None, fromDate=None, toDate=None, page=0, pageSize = 20):
	#przerobic to jakos sensownie
	diseases = ClinvarDisease.objects.all()
	if not name is None:
		diseases = diseases.filter(DiseaseName__contains = name)
	if not gene is None:
		diseases = diseases.filter(Genes__GeneName = name)
	if not fromDate is None:
		diseases = diseases.filter(LastModified__gte = fromDate)
	if not toDate is None:
		diseases = diseases.filter(LastModified__lte = toDate)
	offset = page*pageSize
	return diseases[offset : offset + pageSize]
