## Generic DB Utils

import sys, os
## adodbapi is part of win32all
import adodbapi
adodbapi.adodbapi.verbose = False

from miscutils import *           # checkSum

class ResultSet:
    def __init__(self, metadata, data):
        self.metadata = metadata
        self.data = data
        self.rowIndex = -1
        self.row = None
        
        self.colpos = {}
        self.cols = {}
        ci = -1
        for colInfo in self.metadata:
            ci = ci +1
            col = colInfo[0]
            self.colpos[col] = ci
            self.cols[col] = colInfo
        
    def next(self):
        self.rowIndex = self.rowIndex+1
        if self.rowIndex < len(self.data):
            self.row = self.data[self.rowIndex]
            return True
        else:
            self.row = None
            return False
            
    def get(self, col):
        if self.row is not None:
            if self.cols.has_key(col):
                ci = self.colpos[col]
                # print "colpos of col:%s => %s"%(col, ci)
                return self.row[ci]
        return None

    def getNumRows(self):
        return len(self.data)
    
    def getCols(self):
        return self.metadata
    
def getConn(connStr):
    try:
        conn = adodbapi.connect(connStr)
        return conn
    except:
        print "Failed getting db connection to: %s - error: %s"%(connStr, sys.exc_info()[0])
        return None

def getResultSet(conn, sql):
    try:
        curs = conn.cursor()
        curs.execute(sql)
        rows = curs.fetchall()

        rs = ResultSet(curs.description, rows)        
        return rs
    except:
        print "Failed executing sql: %s - error: %s"%(sql, sys.exc_info()[0])
        for x in sys.exc_info():
            print str(x)
        return []   ## default to blank list
    
def getRows(conn, sql):
    try:
        curs = conn.cursor()
        curs.execute(sql)
        rows = curs.fetchall()
        # curs.close()
        return rows
    except:
        print "Failed executing sql: %s - error: %s"%(sql, sys.exc_info()[0])
        for x in sys.exc_info():
            print str(x)
        return []   ## default to blank list

def selectAndPrintResults(conn, sql, db="?"):
    rows = getRows(conn, sql)
    print "db=%s - sql=%s"%(db, sql)
    for i in range(len(rows)):
        print "\n %s"%( str(rows[i]))

def sp_helptext(dbobject, conn, db="?", purpose="checksum"):
    checksum = None
    try:
        sql = "sp_helptext %s"%(dbobject)
        rows = getRows(conn, sql)
        return "\n".join([str(x) for x in rows])
    except:
        print "Failed in sp_helptext. %s" %(sys.exc_info()[0])
        print sys.exc_info()
        return None

def sp_helptext_checksum(dbobject, conn):
    objdef = sp_helptext(dbobject, conn)
    checksum = checkSum(objdef)
    return checksum

def getSysobjectCols():
    return Sysobject.getSysobjectCols # " name, type, type_desc, schema_id, modify_date "
        
##
def setupConnections(connStrings):
    conns = {}
    for db, connStr in connStrings.items():
        # print connStr
        conn = getConn(connStr)
        if conn is not None:
            print "Created connection to: %s with ConnectionString: %s"%(db, connStr)
            conns[db] = conn
        else:
            print "Failed creating connection to: %s with ConnectionString: %s"%(db, connStr)
    return conns

## conns should be a dictionary/Map of dbname=>connection-Object
def testSql(conns):
    sqls = []
    # sqls.append ("select top 50 user_id, login, lastname, userstat from tt_user where login like '%lemonier' ")
    # sqls.append ("select top 2  user_id, login, lastname, userstat from tt_user order by user_id desc ")
    # sqls.append ("sp_helptext tp_intaudit")

    for sql in sqls:
        for db, conn in conns.items():
            selectAndPrintResults(conn, sql, db)
