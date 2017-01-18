## Bug 44221  -- 102

import os, sys
from os import stat
import xml.etree.ElementTree as ET # Python 2.5
from os.path import join

class XmlProcessorAsn:
    f = None
    tree = None
    fn = None
    paths = None
    cols = "??"
    debugflag = True
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
        print ("init ok")

    def getEstBlDestTime(self):
        # return self.getXmlDoc(self.f)
        return self.getData("/ASN/EstBLDestDate")

    def getTree(self, fp):
        return self.tree


    def getData(self, path):
        val = "?"
        try:
          val = self.tree.findtext(path)
          print "%s --> %s " %(path, val)
        except:
          val = "??"
        return val

    def __str__(self):
        data = []
        for p in self.paths:
            # data.append(self.tree.findtext(p))
            data.append(self.getData(p))
        return "|".join(data)

    def sqlrow(self, tableName):
        data = []
        for p in self.paths:
            data.append(self.getData(p))
        data2 = map(prep, data)
        dataText = ", ".join(data2)
        if (self.cols is None): self.cols = ""
        sql = "insert into %s ( %s ) values ( %s ) " % (tableName, self.cols, dataText)
        print (sql)
        return sql

def prep(s):
    return "'%s'"%(s.replace("'","''"))

def getCreateTable(tableName):
    sql = """create table %s
(
TransactionInfo_MessageSender   varchar(255), 
TransactionInfo_MessageID   varchar(255), 
TransactionInfo_Created     datetime, 
TransactionInfo_FileName    varchar(255), 
ASN_PurposeCode         varchar(255), 
ASN_ShipmentID          varchar(255), 
ASN_ShipmentType        varchar(255), 
ASN_EstBLDestDate       datetime, 
ASN_EstOnBoardDate      datetime, 
ASN_EstDepartDate       datetime, 
ASN_EstDischargePortDate    datetime,

om_cm_id   int,
asnmodtime datetime,
modtime    datetime,
islatest   int




)
""" % (tableName)
    return sql


def processFiles(rootdir):

    errorlog = file("error.log", "w")
    sqlfile = file("createAsns.sql", "w")  
    tableName = "Bug44221_Liz"
    sqlfile.write(getCreateTable(tableName) + "\n\n")
    
    i = 0
    for root, dirs, files in os.walk(rootdir):

        for fn in files:
            i = i +1
            fp = join(root, fn)
            f = file(fp, "r")
            # print "%s / %s " %(fp, fn)
            print "%s " %(fn)

            if not fn.strip().lower().endswith(".xml"):
                continue
            
            try:
                asn = XmlProcessorAsn(f)
                # print a
                sql = asn.sqlrow(tableName)
                # 
                if i % 100 == 0:
                  print "On File # %s Name=%s sql=%s" %(i, fn, sql)
                sqlfile.write(sql + "\n");
            except:
                err = "Failed to generate sql for file: %s -- %s" %(fn, sys.exc_info()[0] )
                print err
                errorlog.write(err + "\n")
            

            if i > 5: return

    sqlfile.write("\n\n-- select * from %s \n"%(tableName))

    sqlfile.close()


debugflag = True

def logdebug(self, msg):
    if debugflag:
        print "%s" %(msg)

# processFiles(r'C:\GT\44287\unzipped');
processFiles(r'C:\GT\44287\test');


