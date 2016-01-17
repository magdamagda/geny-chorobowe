from django.shortcuts import render, redirect
from django.http import HttpResponse
import clinvar, medgen, pubmed
import logging
import logging.handlers
import json

logging.basicConfig(filename='genes.log',level=logging.INFO,format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)
handler = logging.handlers.RotatingFileHandler('genes.log', maxBytes=1024)
logger.addHandler(handler)


def index(request):
    diseases_list, nextPage = clinvar.getDiseasesFromDatabase()
    context = {'diseases_list': diseases_list, 'diseaseName' : "", 'geneSymbol' : "", "fromDate" : "", "toDate" : "", "page" : 0, "nextPage" : nextPage}
    return render(request, 'index.html', context)

def filterDiseases(request):
    diseaseName = request.GET["diseaseName"]
    geneSymbol = request.GET["geneSymbol"]
    fromDate = request.GET["fromDate"]
    toDate = request.GET["toDate"]
    page = int(request.GET["page"])
    diseases_list, nextPage = clinvar.getDiseasesFromDatabase(diseaseName, geneSymbol, fromDate, toDate, page)
    context = {'diseases_list': diseases_list, 'diseaseName' : diseaseName, 'geneSymbol' : geneSymbol, "fromDate" : fromDate, "toDate" : toDate, "page" : page, "nextPage" : nextPage}
    return render(request, 'index.html', context)

def update_clinvar(request):
    try:
        clinvar.updateDiseasesList()
        return HttpResponse(json.dumps({"result" :"OK" }), content_type='application/json')
    except Exception as e:
        logger.error(str(e))
        return HttpResponse(json.dumps({"error" : str(e) }), content_type='application/json')

    
def update_medgen(request):
    try:
        medgen.updateMedgenData()
        return HttpResponse(json.dumps({"result" :"OK" }), content_type='application/json')
    except Exception as e:
        logger.error(str(e))
        context = {'error': str(e)}
        return HttpResponse(json.dumps({"error" : str(e) }), content_type='application/json')

def diseaseDetails(request):
    diseaseId = request.GET["id"]
    context = {}
    disease = clinvar.diseaseDetails(diseaseId)
    if not disease is None:
        context["name"] = disease.DiseaseName
        context["disease"] = disease
        context["genes"] = disease.Genes.all()
    concept = medgen.getConceptDetail(diseaseId)
    if not concept is None:
        context["concept"] = concept
        context["related"] = concept.RelatedConcepts.all()
        context["name"] = concept.Name
    if "name" in context:
        context["sources"] = pubmed.getPubmedPublications(context["name"])
        if "genes" in context:
            pubmed.getGenesPubRelation(context["genes"], context["sources"])
    return render(request, 'diseaseDetails.html', context)

def geneDetails(request):
    geneId = int(request.GET["id"])
    gene = clinvar.geneDetails(geneId)
    diseases = gene.clinvardisease_set.all()
    context={"diseases" : diseases, "gene" : gene, "sources" : pubmed.getPubmedPublications(gene.GeneName)}
    return render(request, 'geneDetails.html', context)

def getGraphDataForDisease(request):
    diseaseId = request.GET["id"]
    level = int(request.GET["level"])
    disease = clinvar.diseaseDetails(diseaseId)
    i=0
    diseases = {} # disease id : disease name
    genes = {} # gene id : gene name
    connections = [] # [[disease id, gene id], ]
    relatedDiseases = [diseaseId, ]
    diseases[disease.ConceptID]=disease.DiseaseName
    while i<level and len(relatedDiseases) > 0:
        relatedGenes = getGenesRelatedToDiseases(relatedDiseases, genes, diseases, connections)
        i += 1
        if i<level:
            relatedDiseases = getDiseasesRelatedToGenes(relatedGenes, genes, diseases, connections)
            i+=1
    return HttpResponse(json.dumps({"data" : {"diseases" : diseases, "genes" : genes, "connections" : connections } }), content_type='application/json')

def getGraphDataForGene(request):
    geneId = int(request.GET["id"])
    level = int(request.GET["level"])
    gene = clinvar.geneDetails(geneId)
    i=0
    diseases = {} # disease id : disease name
    genes = {} # gene id : gene name
    connections = [] # [[disease id, gene id], ]
    relatedGenes = [geneId, ]
    genes[gene.GeneID]=gene.GeneName
    while i<level and len(relatedGenes) > 0:
        relatedDiseases = getDiseasesRelatedToGenes(relatedGenes, genes, diseases, connections)
        i += 1
        if i<level:
            relatedGenes = getGenesRelatedToDiseases(relatedDiseases, genes, diseases, connections)
            i+=1
    return HttpResponse(json.dumps({"data" : {"diseases" : diseases, "genes" : genes, "connections" : connections } }), content_type='application/json')

def getGenesRelatedToDiseases(relatedDiseases, genes, diseases, connections):
    relatedGenesList = []
    for diseaseID in relatedDiseases:
        genesList = clinvar.diseaseGenes(diseaseID)
        for gene in genesList:
            if not gene.GeneID in genes:
                genes[gene.GeneID] = gene.GeneName
                connections.append([diseaseID, gene.GeneID])
                relatedGenesList.append(gene.GeneID)
    return relatedGenesList

def getDiseasesRelatedToGenes(relatedGenes, genes, diseases, connections):
    relatedDiseasesList = []
    for geneID in relatedGenes:
        diseasesList = clinvar.geneDiseases(geneID)
        for disease in diseasesList:
            if not disease.ConceptID in diseases:
                diseases[disease.ConceptID] = disease.DiseaseName
                connections.append([disease.ConceptID, geneID])
                relatedDiseasesList.append(disease.ConceptID)
    return relatedDiseasesList