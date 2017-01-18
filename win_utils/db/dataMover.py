import os, sys
from tbl import *
"""
Aliases:
Table ==> Tbl
Con   ==> Constraint
"""

rootDir = r"c:\gt\DataMover"
pkFile = file(r"%s\PK_FK_distinct.csv"%rootDir)
tblMetaFile = file(r"%s\gtTables.csv"%rootDir)

Tbls = {}
tblTypes = {}

## Cache Tbls
def getTbl(name):
    tbl = None
    if Tbls.has_key(name):
        tbl = Tbls[name]
    else:
        # print "Creating Tbl object: %s"%(name)
        tbl = Tbl(name)
        Tbls[name] = tbl
    return tbl

class Pk:
    def __init__(self, pktblName, pkCol, fktblName, fkCol, fkConstraint = None):
        self.pkTblObj   = getTbl(pktblName)
        self.pkCol = pkCol
        self.fkTblObj   = getTbl(fktblName)
        self.fkCol = fkCol
        self.fkConstraint  = fkConstraint

        ## Object Pk ==>>> tt_om_po.om_po_id <= tt_om_container.om_po_id (tt_om_container_om_po_id_FK)
        ##  - Add this Pk object as a parent to Tbl object: tt_om_container
        self.pkTblObj.addChild(self)
        self.fkTblObj.addParent(self)
        
    def detail(self):
        return "%s.%s <= %s.%s (%s)"%(self.pkTblObj.tblName, self.pkCol, self.fkTblObj.tblName, self.fkCol, self.fkConstraint)    

    def __str__(self):
        return "%s.%s <= %s.%s "%(self.pkTblObj.tblName, self.pkCol, self.fkTblObj.tblName, self.fkCol)    

    def childInfo(self):
        return "%s.%s ==> %s.%s "%(self.child().tblName.ljust(40), self.fkCol.ljust(30), self.parent().tblName, self.pkCol)

    def getColInfo(self):
        pkc = self.pkCol
        fkc = self.fkCol
        if pkc == fkc:
            return " with %s" %(pkc)  ## identical column name
        else:
            return " on %s <= %s "%(pkc, fkc)

    def parentInfo(self):
        # return "%s.%s <<== %s.%s "%(self.parent().tblName.ljust(40), self.pkCol.ljust(30), self.child().tblName, self.fkCol)

        parInfo = "%s (%s)" %(self.parent().tblName, self.parent().tblType)
        return "%s <= %s %s"%(parInfo.ljust(40), self.child().tblName.ljust(40), self.getColInfo())

    def childInfo(self):
        parInfo = "%s (%s)" %(self.parent().tblName, self.parent().tblType)
        return "%s <= %s %s"%(parInfo.ljust(40), self.child().tblName.ljust(40), self.getColInfo())


    def child(self):
        return self.fkTblObj

    def parent(self):
        return self.pkTblObj


## Set meta data
## tt_om_poparty,45270192,11337168 KB,data
for ti in tblMetaFile.readlines():  # ti for TblInfo
    ti = ti.strip().split(",")
    tbl = getTbl(ti[0])
    tbl.setRows(ti[1])
    tbl.setType(ti[3])
    if tbl.tblName == "tt_om_po":
        print tbl

## Loop through constaints
i = 0
for rel in pkFile.readlines():
    rel = rel.strip()
    i = i +1
    if i == 1:
        continue

    pkInfo = rel.split(",")
    pk,pkc,fk,fkc, fkConstraint = pkInfo[0], pkInfo[1], pkInfo[2], pkInfo[3], pkInfo[4]

    myPk = Pk(pk,pkc, fk, fkc, fkConstraint)
    # print myPk

    """    
    if i % 100 == 0:
        print "%s.%s <= %s.%s "%(pk, pkc, fk, fkc)    
        print "%s => %s"%(i, rel)
    """

poTbl = getTbl("tt_om_po")
poTbl.printAll(40, [], True)

poTbl.printAll(40, [], False)
