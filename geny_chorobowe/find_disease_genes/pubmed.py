from urllib2 import urlopen
import httplib, urllib
import httplib2
import xml.etree.ElementTree as ET

pubMedIdsPath = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
pubmedSourcesPath = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def getPubmedPublications(diseaseName):
    ids = getIds(diseaseName)
    return getSourcesDetail(ids)

def getIds(name):
    data = urllib.urlencode({"term" : name})
    h = httplib2.Http()
    resp, content = h.request(pubMedIdsPath + "?" + data , method="GET")
    root = ET.fromstring(content)
    ids = root.find("IdList")
    result = ''
    for i in ids.findall("Id"):
        result += "," + i.text
    return result
    
def getSourcesDetail(ids):
    data = urllib.urlencode({"db" : "pubmed", "id" : ids})
    h = httplib2.Http()
    resp, content = h.request(pubmedSourcesPath + "?" + data, method="GET")
    result = []
    root = ET.fromstring(content)
    docs = root.findall("DocSum")
    for doc in docs:
        d = pubMedDoc()
        d.Id = doc.find("Id").text
        for item in doc.findall("Item"):
            if item.attrib["Name"]=="PubDate":
                d.Data = item.text
            if item.attrib["Name"]=="AuthorList":
                for author in item.findall("Item"):
                    d.Authors.append(author.text)
            if item.attrib["Name"]=="Title":
                d.Title = item.text
            if item.attrib["Name"]=="FullJournalName":
                d.Journal = item.text
        result.append(d)
    return result

class pubMedDoc():
    def __init__(self):
        self.Id = None
        self.Data = None
        self.Authors = []
        self.Title = ""
        self.Journal = ""