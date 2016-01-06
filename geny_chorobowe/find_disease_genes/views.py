from django.shortcuts import render, redirect
from django.http import HttpResponse
import clinvar
import logging
import logging.handlers
logging.basicConfig(filename='genes.log',level=logging.INFO,format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

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
        return redirect('index')
    except Exception as e:
        logger.error(str(e))
        context = {'error': str(e)}
        return render(request, 'error_page.html', context)
    
def diseaseDetails(request):
    diseaseId = int(request.GET["id"])
    disease = clinvar.diseaseDetails(diseaseId)
    genes = disease.Genes.all()
    context={"disease" : disease, "genes" : genes, "source" : disease.SourceID}
    return render(request, 'diseaseDetails.html', context)

def geneDetails(request):
    geneId = int(request.GET["id"])
    gene = clinvar.geneDetails(geneId)
    diseases = gene.clinvardisease_set.all()
    context={"diseases" : diseases, "gene" : gene}
    return render(request, 'geneDetails.html', context)

    
