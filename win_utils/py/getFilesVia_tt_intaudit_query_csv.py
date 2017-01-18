## Expects CSV data
"""
# Testing --> from testMssggrab.py
from mssggrab import *
getMssgDocData(28377510)
getMssgDocData(28377510, "myfile_28377510.xml")

"""

from mssggrab import *

import sys, os
import csv

folder = r"C:\GT\Data\MssgServer\62745"
fnIn = r"%s\vf_614rows.csv" %(folder)

fnIn = r"C:\GT\Bugs\62745_VF_PO_Reprocess\vf_614rows.csv"
if len(sys.argv) > 1:
    fnIn = sys.argv[1]

dataReader = csv.DictReader(file(fnIn), delimiter=",", quotechar='"')


numFiles = 0

for row in dataReader:
    numFiles = numFiles +1
    filename = row.get('filename')
    filenameRoot = os.path.splitext(filename)[0]
    mssg_doc_id = row.get('mssgdoc_id') or row.get('mssg_doc_id')

    newFileName = "%s_%s.xml"%(filenameRoot, mssg_doc_id)

    print ("Writing %s to %s"%(newFileName, folder))
    getMssgDocData(mssg_doc_id, newFileName, folder)


print "Wrote %s files to %s" %(numFiles, folder)
