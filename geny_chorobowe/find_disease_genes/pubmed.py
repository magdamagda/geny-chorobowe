import urllib
import httplib2
import xml.etree.ElementTree as ET
from datetime import datetime

pubMedIdsPath = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
pubmedSourcesPath = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def getPubmedPublications(diseaseName):
    ids = getIds(diseaseName)
    result = ''
    for i in ids:
        result += "," + i
    return getSourcesDetail(result)

def getIds(name):
    data = urllib.urlencode({"term" : name})
    h = httplib2.Http()
    resp, content = h.request(pubMedIdsPath + "?" + data , method="GET")
    root = ET.fromstring(content)
    ids = root.find("IdList")
    result = []
    for i in ids.findall("Id"):
        result.append(i.text)
    return result
    
def getSourcesDetail(ids):
    data = urllib.urlencode({"db" : "pubmed", "id" : ids})
    h = httplib2.Http()
    resp, content = h.request(pubmedSourcesPath + "?" + data, method="GET")
    result = []
    root = ET.fromstring(content)
    docs = root.findall("DocSum")
    i=1
    for doc in docs:
        d = pubMedDoc()
        d.Id = doc.find("Id").text
        d.Num = i
        for item in doc.findall("Item"):
            if item.attrib["Name"]=="PubDate":
                #lastmod = datetime.strptime(pola[7], '%d %b %Y').strftime('%Y-%m-%d')
                d.PubDate = item.text
            if item.attrib["Name"]=="History":
                for date in item.findall("Item"):
                    if date.attrib["Name"] == "pubmed":
                        d.Date = date.text
            if item.attrib["Name"]=="AuthorList":
                for author in item.findall("Item"):
                    d.Authors.append(author.text)
            if item.attrib["Name"]=="Title":
                d.Title = item.text
            if item.attrib["Name"]=="FullJournalName":
                d.Journal = item.text
        result.append(d)
        i+=1
    return result

def getGenesPubRelation(genes, pubs):
    for gene in genes:
        ids = getIds(gene.GeneName)
        for pub in pubs:
            if pub.Id in ids:
                print "appending"
                pub.related.append({"name" : gene.GeneName, "id" : gene.GeneID})

class pubMedDoc():
    def __init__(self):
        self.Id = None
        self.PubDate = ""
        self.Date = None
        self.Authors = []
        self.Title = ""
        self.Journal = ""
        self.Num = 0
        self.related = []