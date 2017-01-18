## Bug 44221

import os, sys
from os import stat
from os.path import join

# from xml.dom import minidom
# from xml import xpath

# import elementtree.ElementTree as ET
# import cElementTree as ET
# import lxml.etree as ET
import xml.etree.ElementTree as ET # Python 2.5

class XmlProcessorAsn:
    f = None
    tree = None
    fn = None
    paths = None
    cols = "??"
    def __init__(self, f):
        self.f = f
        self.tree = ET.parse(f.name)
        self.fn = os.path.split(f.name)[1]
        self.paths = []
        paths = self.paths
        paths.append('TransactionInfo/MessageSender')
        paths.append('TransactionInfo/MessageID')
        paths.append('TransactionInfo/Created')
        paths.append('TransactionInfo/FileName')
        paths.append('ASN/PurposeCode')
        paths.append('ASN/ShipmentID')
        paths.append('ASN/ShipmentType')
        paths.append('ASN/EstBLDestDate')
        paths.append('ASN/EstOnBoardDate')
        paths.append('ASN/EstDepartDate')
        paths.append('ASN/EstDischargePortDate')

        pc = []
        for p in paths:
            pc.append(p.replace("/","_"))
        self.cols = ", ".join(pc)

    def isCrossBorder(self):
        return self.getDataForXpath('ASN/ShipmentType').lower() == 'crossborder'

    def getEstBlDestTime(self):
        # return self.getXmlDoc(self.f)
        return self.tree.findtext("/ASN/EstBLDestDate")

    def getTree(self, fp):
        return self.tree


    def __str__(self):
        data = []
        for p in self.paths:
            data.append(self.getDataForXpath(p))
        return "|".join(data)

    def sqlrow(self, tableName):
        data = []
        for p in self.paths:
            # data.append(self.tree.findtext(p))  # no try/except, need one
            data.append(self.getDataForXpath(p))

        data2 = map(prep, data)
        dataText = ", ".join(data2)
        if (self.cols is None): self.cols = ""
        sql = "insert into %s ( %s ) values ( %s ) " % (tableName, self.cols, dataText)
        return sql

    def getDataForXpath(self, myxpath):
        rc = ''
        try:
          rc = self.tree.findtext(myxpath)
        except:
          rc = ''
        if rc is None:
          rc = ''

        return rc

def prep(s):
    if len(s) > 0:
        return "'%s'"%(s.replace("'","''"))
    else:
        return "null";

def getCreateTable(tableName):
    sql = """create table %s
(
TransactionInfo_MessageSender	varchar(255), 
TransactionInfo_MessageID	varchar(255), 
TransactionInfo_Created		datetime, 
TransactionInfo_FileName	varchar(255), 
ASN_PurposeCode			varchar(255), 
ASN_ShipmentID			varchar(255), 
ASN_ShipmentType		varchar(255), 
ASN_EstBLDestDate		datetime, 
ASN_EstOnBoardDate		datetime, 
ASN_EstDepartDate		datetime, 
ASN_EstDischargePortDate	datetime,

om_cm_id int,
asnmodtime datetime,
modtime datetime default getdate(),
islatest int


)
""" % (tableName)
    return sql


def processFiles(rootdir):

    
    sqlfile = file("createAsns.sql", "w")  
    tableName = "Bug44287_wsi"
    sqlfile.write(getCreateTable(tableName) + "\n\n")
    
    fnum = 0; i=0; fok=0; ffailed=0;
    notcb = 0;
    for root, dirs, files in os.walk(rootdir):

        for fn in files:
            fp = join(root, fn)
            f = file(fp, "r")
            # print "%s / %s " %(fp, fn)
            
            fnum = fnum + 1

            if not fn.strip().lower().endswith(".xml"):
                continue

            i = i +1    # xml files = i
            print "%s --> %s " %(i, fn)

            try:
                asn = XmlProcessorAsn(f)
                # print a

                if not asn.isCrossBorder():
                  # print "   %s --> %s - Not Cross-Border, not writing. " %(i, fn)
                  notcb = notcb+1
                  continue

                sql = asn.sqlrow(tableName)
                # 
                if i % 100 == 0:
                  print "On File # %s Name=%s sql=%s" %(i, fn, sql)
                sqlfile.write(sql + "\n");
                fok = fok+1
            except:
                ffailed = ffailed + 1
                err = "Failed to generate sql for file: %s -- %s " %(fn, sys.exc_info())
                # print err
                logError (err)
                # errorlog.write(err + "\n")

            # if i > 5: return
            
    ## Summary ...
    print ("fnum=%s xmlFiles=%s fok=%s ffailed=%s not-CrossBorder=%s "%(fnum, i, fok, ffailed,notcb))


    sqlfile.write("\n\n-- select * from %s \n"%(tableName))
    sqlfile.close()

    errorlog.close()
    
# processFiles('./Archive')

def logError(errText):
  errorlog.write(errText + "\n")

errorlog = file("error.log", "w")

# processFiles(r'C:\GT\44221\csi');
processFiles(r'C:\GT\44287\unzipped');




