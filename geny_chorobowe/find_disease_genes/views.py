from django.shortcuts import render
from django.http import HttpResponse
import clinvar

def index(request):
    diseases_list = clinvar.getDiseasesList()
    context = {'diseases_list': diseases_list}
    return render(request, 'index.html', context)
