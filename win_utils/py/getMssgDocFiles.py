# Expects 1st parameter to be filename containing mssg_doc_id's 1-per-line
# Products 123.xml, 456.xml, etc.

import os
from mssggrab import *

fn = "mssgdocids.txt"
if len(sys.argv) > 1:
    fn = sys.argv[1]

folder = ".\\MssgDocFiles"
if len(sys.argv) > 2:
    folder = sys.argv[2]

if not os.path.exists(folder):
    os.makedirs(folder)

fMssgDocIds = file(fn)

for mssg_doc_id in fMssgDocIds.readlines():
    mssg_doc_id = mssg_doc_id.strip()

    if (len(mssg_doc_id) > 1):
        print mssg_doc_id
        newFileName = "%s.xml"%(mssg_doc_id)

        print ("Writing %s to %s"%(newFileName, folder))
        getMssgDocWriteData(mssg_doc_id, None, folder)

fMssgDocIds.close()
