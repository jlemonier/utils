import os, sys
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

class Tbl:
    def __init__(self, tblName):
        self.tblName = tblName
        self.parents = []
        self.children = []
        self.tblType = "data"  ## default

    def __str__(self):
        return "%s parents: %s children: %s "%(self.tblName, len(self.parents), len(self.children))

    def addParent(self, pkObject):
        if not pkObject in self.parents:
            self.parents.append(pkObject)
            self.parents.sort(key = lambda pk : pk.parent().tblName)

    def addChild(self, pkObject):
        if not pkObject in self.children:
            self.children.append(pkObject)
            self.children.sort(key = lambda pk : pk.child().tblName)

    def setRows(self, rows):
        self.rows = rows
    ## data or static
    def setType(self, tblType):
        self.tblType = tblType

    def isData(self):
        return self.tblType == "data"
    
    """
    def printFamily(self, xlist, xtype, recursiveParents=False, recursiveChildren=False, indent = 0):
        print "%s Tbl: %s has %s ... "%(" "*indent, self.tblName, xtype)
        for pk in xlist:
            print "%s     %s"%(" "*indent, pk)
            if recursiveParents:
                parent = pk.pkTblObj
                print "         %s"%(parent)
                for pp in parent.parents:
                    print "             %s"%(pp)
                # parent.printParents(recursiveParents, indent+1)
            if recursiveChildren:
                child = pk.fkTblObj
                print "         %s"%(child)
                # child.printChildren(recursiveChildren, indent+1)
    """

    def printAll(self, indent = 40, TblsPrinted = [], recurse = False):
        TblsPrinted.append(self)
        
        print "%s%s"%(" "*indent, "*"*80)
        print "%s*** Starting Printing Tbl: %s Recursive=%s ***"%(" "*indent, self.tblName, recurse)
        print "%s%s"%(" "*indent, "*"*80)
        
        self.printParents(indent - 4, TblsPrinted, recurse)
        
        print "%s%s"%(" "*indent, "*"*80)
        print "%s*** %s **  (parents printed above, children below)"%(" "*indent, self.tblName)
        print "%s%s"%(" "*indent, "*"*80)
        
        self.printChildren(indent + 4, TblsPrinted, recurse)

        print "%s%s"%(" "*indent, "*"*80)
        print "%s*** End Printing Tbl: %s ***"%(" "*indent,self.tblName)
        print "%s%s"%(" "*indent, "*"*80)

    def printChildren(self, indent=0, TblsPrinted = [], recurse = False):
        ## self.printFamily(self.children, "Children", False, recursive, indent = 0)
        for childPk in self.children:
            child = childPk.child()
            print "%s %s "%(" "*(indent), child.tblName)
            print "%s %s (%s)"%(" "*(indent+2), childPk.childInfo(), child.tblType)
            if recurse:
                child.printChildren(indent +4)            
            
            # childPk.fkTblObj.printAll()

    def printParents(self, indent=0, TblsPrinted = [], recurse = False):
        for parentPk in self.parents:
            parent = parentPk.parent()
            if not parent in TblsPrinted:
                if recurse:
                    parent.printParents(indent-4)

                print "%s %s (%s) "%(" "*indent, parentPk.parentInfo(), parent.tblType)
    

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
