"""
\\jlemonier\gt\bugs\vf\62745\VF_reprocess_failed_files_intaudit.sql
 to generate resultset => xls => csv

"""

from mssggrab import *
from xsdHide1 import *

import sys, os
import csv

fnIn = r"C:\GT\Bugs\VF\62745\nov1_reprocess.csv"

outputFolder = []
outputFolder.append(r"C:\GT\Bugs\VF\62745\po_oct28\in\purchase_order\xml3")
outputFolder.append(r"Q:\in\purchase_order\xml3")

dataReader = csv.DictReader(file(fnIn), delimiter=",", quotechar='"')
numFiles = 0

for folder in outputFolder:
    if not os.path.exists(folder):
        os.makedirs(folder)

def writeFile(folder, filename, data):
    print ("Writing %s to %s"%(filename, folder))
    filePath = r"%s\%s"%(folder, filename)
    fOut = file(filePath, "w")
    fOut.write(data)
    fOut.close()    

for row in dataReader:
    numFiles = numFiles +1
    filename = row.get('filename')
    filenameRoot = os.path.splitext(filename)[0]
    mssg_doc_id = row.get('mssgdoc_id') or row.get('mssg_doc_id')

    newFileName = "%s_%s.xml"%(filenameRoot, mssg_doc_id)

    
    data = getMssgDocData(mssg_doc_id)
    data2 = hideElements(data)

    for folder in outputFolder:
        writeFile(folder, newFileName, data2)    
    
