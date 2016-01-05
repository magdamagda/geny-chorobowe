from django.shortcuts import render, redirect
from django.http import HttpResponse
import clinvar
import logging
import logging.handlers
logging.basicConfig(filename='genes.log',level=logging.INFO,format='%(asctime)s.%(msecs)d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger(__name__)

def index(request):
    diseaseName = request.POST["diseaseName"]
    geneSymbol = request.POST["geneSymbol"]
    fromDate = request.POST["fromDate"]
    toDate = request.POST["toDate"]
    diseases_list = clinvar.getDiseasesFromDatabase(diseaseName, geneSymbol, fromDate, toDate)
    context = {'diseases_list': diseases_list}
    return render(request, 'index.html', context)

def update_clinvar(request):
    try:
        clinvar.updateDiseasesList()
        return redirect('index')
    except Exception as e:
        logger.error(str(e))
        context = {'error': str(e)}
        return render(request, 'error_page.html', context)
