"""geny_chorobowe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
import find_disease_genes.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
	url(r'^update_clinvar$',  find_disease_genes.views.update_clinvar),
    url(r'^update_medgen$',  find_disease_genes.views.update_medgen),
	url(r'^$',  find_disease_genes.views.index, name='index'),
    url(r'^filterDiseases$',  find_disease_genes.views.filterDiseases),
    url(r'^diseaseDetails$',  find_disease_genes.views.diseaseDetails),
    url(r'^geneDetails$',  find_disease_genes.views.geneDetails),
    url(r'^getGraphDataForDisease$',  find_disease_genes.views.getGraphDataForDisease),
    url(r'^getGraphDataForGene$',  find_disease_genes.views.getGraphDataForGene),
]
