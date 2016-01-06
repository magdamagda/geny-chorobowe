from urllib2 import urlopen
from datetime import datetime
import gzip

def donloadAndUnzip(path):
    req = urlopen(path)
    data = req.read()
    gzip.decompress(data)
