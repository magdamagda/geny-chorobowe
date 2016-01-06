from urllib2 import urlopen
from datetime import datetime
from django.db import transaction
from models import *
import logging

logger = logging.getLogger(__name__)

sourcePath = "ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/gene_condition_source_id"

def updateDiseasesList():
	#na poczatek wywalic wszystkie choroby z bazy
	ClinvarDisease.objects.all().delete()
	ClinvarSource.objects.all().delete()
	ClinvarGene.objects.all().delete()
	#i sciagnac wszystkie od nowa
	req = urlopen(sourcePath)
	data = req.read()
	diseases = {}
	genesDict = {}
	genes = {}
	sources = {}
	lines = data.split("\n")
	lines.pop(0)
	for line in lines:
		if len(line)>0:
			pola = line.split("\t")
			lastmod = datetime.strptime(pola[7], '%d %b %Y').strftime('%Y-%m-%d')
			concept = pola[2]
			sourceId = convertToIntIfPossible(pola[5])
			diseases[concept]=[pola[3], sourceId, pola[6], lastmod] #concept : name, sourceID, mim, last_mod
			if not concept in genesDict:
				genesDict[concept] = []
			genesDict[concept].append(pola[0])
			genes[pola[0]] = pola[1] #id : name
			if not sourceId == None:
				sources[pola[5]]= pola[4] #id : name

	#insert genes
	with transaction.atomic():
		for g in genes:
			ClinvarGene.objects.create(GeneName = genes[g] , GeneID = g)

	#insert sources
	with transaction.atomic():
		for s in sources:
			ClinvarSource.objects.create(SourceName = sources[s] , SourceID = s)
			
	#insert diseases
	with transaction.atomic():
		for d in diseases:
			SourceID=None
			if not diseases[d][1] is None:
				source = ClinvarSource.objects.get(SourceID=diseases[d][1])
			disease = ClinvarDisease(DiseaseName = diseases[d][0], Source = source, LastModified = diseases[d][3], ConceptID=d, DiseaseMIM = diseases[d][2] )
			disease.save()
			for gene in genesDict[d]:
				disease.Genes.add(ClinvarGene.objects.get(GeneID = gene))

def getDiseasesFromDatabase(name=None, gene=None, fromDate=None, toDate=None, page=0, pageSize = 20):
	diseases = ClinvarDisease.objects.all()
	if not name is None and not name=="":
		diseases = diseases.filter(DiseaseName__contains = name)
	if not gene is None and not gene=="":
		diseases = diseases.filter(Genes__GeneName = name)
	if not fromDate is None and not fromDate=="":
		diseases = diseases.filter(LastModified__gte = fromDate)
	if not toDate is None and not toDate=="":
		diseases = diseases.filter(LastModified__lte = toDate)
	diseases=diseases.order_by('-LastModified')
	offset = page*pageSize
	diseases = diseases[offset : offset + pageSize + 1]
	nextPage=False
	if len(diseases) > pageSize:
		nextPage = True
	return diseases[0:20], nextPage

def convertToIntIfPossible(val):
	try:
		return int(val)
	except Exception:
		return None
	
def diseaseDetails(ID):
	disease = ClinvarDisease.objects.get(id = ID)
	return disease

def geneDetails(ID):
	gene = ClinvarGene.objects.get(GeneID = ID)
	return gene
