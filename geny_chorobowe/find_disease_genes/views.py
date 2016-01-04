from django.shortcuts import render
from django.http import HttpResponse
import clinvar

def index(request):
    diseases_list = clinvar.getDiseasesFromDatabase()
    context = {'diseases_list': diseases_list}
    return render(request, 'index.html', context)

def update_clinvar(request):
    try:
        clinvar.updateDiseasesList()
        return redirect('index')
    except Exception as e:
        context = {'error': str(e)}
        return render(request, 'error_page.html', context)
