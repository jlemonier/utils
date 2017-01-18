## import os, sys
"""
Tbl object is a node in the graph (tree) of tables
    addParent
    addKid
    getParents
    getKids
"""

class Tbl:
    def __init__(self, tblName):
        self.tblName = tblName
        self.parents = []
        self.children = []
        self.tblType = "data"  ## default

    def __str__(self):
        return "%s parents: %s children: %s "%(self.tblName, len(self.parents), len(self.children))

    def getParents(self):
        return self.parents
    
    def getChildren(self):
        return self.children
    ## Alias
    def getKids(self):
        return self.getChildren()

    def addParent(self, pkObject):
        if not pkObject in self.parents:
            self.parents.append(pkObject)
            self.parents.sort(key = lambda pk : pk.parent().tblName)

    def addChild(self, pkObject):
        if not pkObject in self.children:
            self.children.append(pkObject)
            self.children.sort(key = lambda pk : pk.child().tblName)
    
    def addKid(self, pkObject):
        self.addChild(pkObject)

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
    
