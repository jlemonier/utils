## columnWithFilePath datafile

import sys, os, urllib2, re
import xml.etree.ElementTree as ET # Python 2.5

col = "filepath"
inputFileName = r"c:\gt\warnaco\payment_terms\inputFile.csv"
if len(sys.argv) >= 2:
    inputFileName = sys.argv[1]

outputFileName = "%s.output.csv" %(inputFileName)
errorFileName = "%s.outputPlusError.log" %(inputFileName)
fout = file(outputFileName, "w")
ferr = file(errorFileName, "w")

print "Input  File: %s"%(inputFileName)
print "Output File: %s"%(outputFileName)
print "Output Plus Error  File: %s"%(errorFileName)

def writeOut(msg):
    print (msg)
    ferr.write("%s\n"%msg)
    fout.write("%s\n"%msg)

def writeErr(msg):
    print("ERROR: %s"%msg)
    ferr.write("ERROR: %s\n"%msg)

def getUrlForFilePath(filePath):
    fileName = os.path.basename(filePath)
    url = "http://pfile1a/file_search_results.asp?EnvironmentType=prod&MessageType=orders&FileNameValue=%s" %(fileName)
    # print url
    info = getData(url)
    headEndIndex = info.find("</HEAD>")+7
    # print "info before: %s"%info # good
    if headEndIndex <= 0:
        headEndIndex = 0
    info = info[headEndIndex:]
    info = re.sub("[\r\n]", "", info)
    # print "info after 1: %s \n"%info # good

    info2 = info.split("|")
    dataUrl = ""
    if len(info2) >= 4:
        dataUrl = info2[3]
    else:
        writeErr ("-- urlForFilePath(%s) ==> %s" %(filePath, info2))
    return dataUrl


def getData(url):
    try:
        pipe = urllib2.urlopen(url)
        data = pipe.read()
        return data
    except:
        writeErr("no data from url=%s "%(url))
        return "-- data?"
    
def getDataForUrl(url):
    return getData(url)

tags = []
tags.append("Order/Header/OrderMessageID")
tags.append("Order/Header/OrderNumber")
tags.append("Order/Header/OrderDateTime")
tags.append("Order/Header/PaymentTerms")
tags.append("Order/Header/OrderPaymentMethod/")
tags.append("Order/Header/OrderPaymentTerms/PaymentTerms")
tagsText = " , ".join(tags)
tagsText = tagsText.replace("/","_")
writeOut("ponum , om_po_id , intaudit_id, payment_terms_orig , filepath, url, %s" %(tagsText))

fin = file(inputFileName)
hdr = fin.readline()
hdr = []
i = 0
for line in fin.readlines():
    line = line.strip()
    i = i + 1
    if i > 999999:
        break
    
    ponum,om_po_id,intaudit_id,payment_terms_orig,filepath = line.split(",")
    url = getUrlForFilePath(filepath)
    data = getDataForUrl(url)
    # print "%s %s %s " %(ponum, filepath, url)
    
    # xmlTreePo = ET.parse(fileName)
    try:
        xmlTreePo = ET.fromstring(data)
    except:
        print "-- Failed to parse data=%s from line=%s"%(data[:50], line)
    tagInfos = []
    for tag in tags:
        try:
            el = xmlTreePo.findtext(tag)
            # print "-- %s: %s=%s"%(ponum, tag, el)     ## handy for debugging, not for excel
            tagInfos.append("%s"%el)
        except:
            writeErr("-- Failed to findtext for xpath=%s"%(tag))
    tagInfosText = ",".join(tagInfos)
    
    writeOut("%s,%s,%s,%s,%s,%s,%s"%(ponum , om_po_id , payment_terms_orig , intaudit_id, filepath, url, tagInfosText))

    xmlfn = r"xml\%s"%os.path.basename(filepath)
    print "Creating file %s"%xmlfn
    poxml = file(xmlfn, "w+")
    poxml.write(data)
    poxml.close()
    

fin.close()
fout.close()
ferr.close()
