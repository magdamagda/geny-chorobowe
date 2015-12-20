from urllib2 import urlopen

def getDiseasesList():
    req = urlopen('ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/disease_names')
    data = req.read()
    diseases = []
    lines = data.split("\n")
    for line in lines:
        if len(line)>0:
            diseases.append(line.split("\t")[0])
    return diseases[1:]
