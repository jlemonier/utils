import csv, sys, urllib2, os
from findPoData import *

def getXml(mssgdoc_id):
    # check if file: "$mssgdoc_id.xml" exists already, if so, do not get it again
    mssgdocFileName = r"xml\\%s.xml"%(mssgdoc_id)
    
    if os.path.exists(mssgdocFileName):
        x = 2
        # print ("%s exists already.  Not retrieving again."%(mssgdocFileName))
    else:
        url =  r"https://network.gtnexus.com/sysmgmt/mssggrab_sitescope.jsp?mssgdocid=%s"%(mssgdoc_id)
        data = getData(url)
        outFile = file(mssgdocFileName, "w")
        outFile.write(data)
        outFile.close()

    return mssgdocFileName

def getData(url):
    try:
        pipe = urllib2.urlopen(url)
        xdata = pipe.read()
        return xdata
    except:
        # writeErr("no data from url=%s "%(url))
        printEx(sys.exc_info())
        return None    

def printEx(ex):
    for x in ex:
        print str(x)
    tb = ex[2]
    # traceback.print_tb(tb)

"""
	Supplier => ['NGCJBA_VFC_PO_13QQK6_20100611T024904_Update', '13QQK6', 'EUC0058637', 'EU TEXPORT INDUSTRIES PVT LTD', 'INBLR', 'UN']

<PartyInfo>
 <Type>Supplier</Type> 
 <Code>EUC0058637</Code> 
 <Name>EU TEXPORT INDUSTRIES PVT LTD</Name> 
 <City>
  <CityCode Qualifier="UN">INBLR</CityCode> 
 </City>
</PartyInfo>

	
"""
def getPartyInfoDisplay(info, partyType):
    if info is None:
        info = []
    for i in range(1,7):
        info.append("")
    # pstr = "CityCode|%s|Qualifier|%s|Code|%s|Name|%s|PO#|%s|FileName|%s|"%(info[4], info[5], info[2], info[3], info[1], info[0] )
    pstr = "%s|%s|%s|%s|%s|%s|%s|"%(partyType, info[4], info[5], info[2], info[3], info[1], info[0] )
    return pstr.strip()
    

fileNameIntauditResults = "city_sev2.csv"
fnResults = file(fileNameIntauditResults)
# csvReader = csv.reader(fnResults, delimiter=',', quotechar='"')
csvReader = csv.DictReader(fnResults, delimiter=',', quotechar='"')

i = 0

fnOut = file("%s.out"%(fileNameIntauditResults), "w")

baseHdr = "PONum|intaudit_id|mssgdoc_id|filename2|reasontext|PartyType|CityCode|Qualifier|Code|Name|PO#|FileName|"
print baseHdr
fnOut.write("%s\n"%(baseHdr))

for row in csvReader:
    i = i + 1
    # {'primary_org_id': '12408', 'controlnum': '45YS039_20100611T024904', 'ponum': '45YS039', 'headercontrolnum': '45YS039_20100611T024', 'mssgdoc_id': '28376802', 'reasontext': 'PO 45YS039 ADD was accepted with warnings with ID: 8840905   //   City could not be resolved for the following parties: EU VE10 StNik ABX VF Shipping Whs (VE10) (ShipTo) |  ', 'intaudit_id': '1134291172', 'reasoncode': '0', 'createtime': '28:01.1'}  

    mssgdoc_id = row['mssgdoc_id']
    fnPoXml = getXml(mssgdoc_id)
    poInfo = DataPrinter(fnPoXml)
    partyInfo = poInfo.getData()
    rt = row['reasontext'].replace("|", "`")
    base = "%s|%s|%s|%s|%s"%(row['ponum'], row['intaudit_id'], row['mssgdoc_id'], fnPoXml, rt) 
    # print base

    for pt in partyInfo.keys():
        if rt.find("(%s)"%(pt)) > 0:
            failedType = "%s|%s"%(base, getPartyInfoDisplay(partyInfo[pt], pt))
            if i % 100 == 0:
                print failedType
            fnOut.write ("%s\n" %failedType)

    # print "%s"%(file(fnPoXml).read())

    testMode = False
    if testMode:
        if i > 5:
            break

fnOut.close()
