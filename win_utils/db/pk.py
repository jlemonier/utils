# import os, sys
"""
Pk
    
"""

class Pk:
    # def __init__(self, pktblName, pkCol, fktblName, fkCol, fkConstraint = None):
    def __init__(self, pkTblObj, pkCol, fkTblObj, fkCol, fkConstraint = None):
        self.pkTblObj   = pkTblObj
        self.pkCol = pkCol
        self.fkTblObj   = fkTblObj
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

