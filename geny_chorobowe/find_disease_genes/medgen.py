from urllib2 import urlopen
from datetime import datetime
import gzip
import os
from models import MedgenConcept
import logging
from django.db import transaction

logger = logging.getLogger(__name__)
conceptDefPath = "ftp://ftp.ncbi.nlm.nih.gov/pub/medgen/MGDEF.RRF.gz"
conceptsRelatedPath = "ftp://ftp.ncbi.nlm.nih.gov/pub/medgen/MGREL.RRF.gz"
conceptNamesSourcesPath = "ftp://ftp.ncbi.nlm.nih.gov/pub/medgen/NAMES.RRF.gz"

def downloadAndUnzip(path):
    req = urlopen(path)
    data = req.read()
    with open('file.txt.gz', 'wb') as f:
        f.write(data)
    with gzip.open('file.txt.gz', 'rb') as f:
        file_content = f.read()
    os.remove('file.txt.gz')
    lines = file_content.split("\n")
    lines.pop(0)
    return lines[0:-1]

def updateMedgenData():
    print "update medgen data"
    MedgenConcept.objects.all().delete()
    defs = getConceptDefs()
    namesAndSources = getNamesAndSources()
    related = getRelatedConcepts()
    print "inserting into db"
    with transaction.atomic():
        for c in defs:
            concept = MedgenConcept.objects.create(ConceptID = c, Name = namesAndSources[c][0], Def = defs[c], Source = namesAndSources[c][1])
            #concept.save()
    print 'defs inserted'
    relatedLen = str(len(related))
    with transaction.atomic():
        i=0
        for c in related:
            print "progres: " + str(i) + "/" + relatedLen
            i+=1
            try:
                concept = MedgenConcept.objects.get(ConceptID = c)
                #concept.RelatedConcepts.add(MedgenConcept.objects.get(ConceptID = c[1]))
                #print c[0] + "  " + c[1]
            except Exception as e:
                print "No concept " + c
            for item in related[c]:
                try:
                    concept.RelatedConcepts.add(MedgenConcept.objects.get(ConceptID = item))
                except Exception as e:
                    print "no concept " + item
                    
def getConceptDefs():
    print "get concept defs"
    conceptsDefs = {}
    lines = downloadAndUnzip(conceptDefPath)
    print "downloaded"
    for line in lines:
        line = line.split("|")
        conceptsDefs[line[0]] = line[1]
    return conceptsDefs
        
def getNamesAndSources():
    print "get names and sources"
    namesAndSources = {}
    lines = downloadAndUnzip(conceptNamesSourcesPath)
    print "downloaded"
    for line in lines:
        line = line.split("|")
        namesAndSources[line[0]] = [line[1], line[2]]
    return namesAndSources

def getRelatedConcepts():
    print "get related concepts"
    related={}
    lines = downloadAndUnzip(conceptsRelatedPath)
    print "downloaded"
    for line in lines:
        line = line.split("|")
        cui1 = line[0]
        cui2 = line[4]
        if not cui1 in related:
            related[cui1] = set()
        related[cui1].add(cui2)
    return related

def getConceptDetail(conceptID):
    try:
        return MedgenConcept.objects.get(ConceptID = conceptID)
    except Exception as e:
        logger.info(str(e))
        print "no concept " + conceptID
        return None

def getConceptByName(name):
    print "get concept by name"
    try:
        return MedgenConcept.objects.get(Name = name)
    except Exception as e:
        print "no concept " + name
        return None

