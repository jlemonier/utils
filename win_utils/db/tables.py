import os, sys

from tbl import *
from pk import *
"""
Aliases:
Table ==> Tbl
Con   ==> Constraint
"""

class Tables:
    
    def __init__(self):
        self.setMetaDataFiles()
        self.loadMetaDataViaFiles()

    ## Cache Tbls
    def getTbl(self, name):
        tbl = None
        if self.Tbls.has_key(name):
            tbl = self.Tbls[name]
        else:
            # print "Creating Tbl object: %s"%(name)
            tbl = Tbl(name)
            self.Tbls[name] = tbl
        return tbl
        
    def setMetaDataFiles(self
                 , rootDir = r"c:\gt\DataMover"
                 , pkFileName = "PK_FK_distinct.csv"
                 , tblMetaFileName = "gtTables.csv"):
        self.rootDir = rootDir
        self.pkFile = file(r"%s\%s"%(rootDir, pkFileName))
        self.tblMetaFile = file(r"%s\%s"%(rootDir, tblMetaFileName))
        
    def loadMetaDataViaFiles(self):
        self.Tbls = {}
        self.tblTypes = {}
        ## Set meta data
        ## tt_om_poparty,45270192,11337168 KB,data
        for ti in self.tblMetaFile.readlines():  # ti for TblInfo
            ti = ti.strip().split(",")
            tbl = self.getTbl(ti[0])
            tbl.setRows(ti[1])
            tbl.setType(ti[3])
            if tbl.tblName == "tt_om_po":
                print tbl
        
        ## Loop through constaints
        i = 0
        for rel in self.pkFile.readlines():
            rel = rel.strip()
            i = i +1
            if i == 1:
                continue
        
            pkInfo = rel.split(",")
            pkt,pkc,fkt,fkc, fkConstraint = pkInfo[0], pkInfo[1], pkInfo[2], pkInfo[3], pkInfo[4]
        
            myPk = Pk(self.getTbl(pkt),pkc, self.getTbl(fkt), fkc, fkConstraint)
            # print myPk
        
            """    
            if i % 100 == 0:
                print "%s.%s <= %s.%s "%(pk, pkc, fk, fkc)    
                print "%s => %s"%(i, rel)
            """
        

    def testPrintTable(self, tblName = "tt_om_po", recurse = True):
        testTbl = self.getTbl(tblName)
        testTbl.printAll(40, [], recurse)
        # testTbl.printAll(40, [], False)


