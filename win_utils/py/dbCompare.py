## Python 2.6.x
## Python add-on: win32all (Windows 7 64-bit version, or XP 32-bit)

## For Sql-Server auth to pnetdb1a using engdbread, needed to create ODBC connection "pnetdb1a"
## For qamain1 and any others, no ODBC setup needed

import os
import sys
import pickle
## Organizing code, putting functions in dbutils.py and miscutils.py modules
from dbutils import *
from miscutils import *
from sysobject import *

## Globals
workDir = r"C:\share\dbcompare"

def setConnStrings(connStrings):
    dbInfo = {}

    # dbServer = 'qamaindb1'
    # dbInfo['qamain1'] = dbServer
    # dbInfo['mssg_qamain1'] = dbServer
    # dbInfo['PSOTimeManagement'] = dbServer

    dbServer = 'qamiscdb1'
    # dbInfo['devmain1'] = dbServer
    dbInfo['STAGE1'] = dbServer

    # dbServer = 'qalivedb1'
    # dbInfo['qalive1'] = dbServer
    # dbInfo['devlive1'] = dbServer

    for db,server in dbInfo.iteritems():        
        connStrings[db] = r"Initial Catalog=%s; Data Source=%s; Provider=SQLOLEDB.1; Integrated Security=SSPI" %(db , server)
        
    connStrings["newtradmarket"] = "DSN=pnetdb1a;  Uid=engdbread; Pwd=(^P1t^!s$"
    
    # connStrings["qamain1"]  = r"Initial Catalog=%s; Data Source=%s; Provider=SQLOLEDB.1; Integrated Security=SSPI" %("qamain1" , "qamaindb1")
    # connStrings["devlive1"] = r"Initial Catalog=%s; Data Source=%s; Provider=SQLOLEDB.1; Integrated Security=SSPI" %("devlive1", "qalivedb1")
    # connStrings["demain1"]  = r"Initial Catalog=%s; Data Source=%s; Provider=SQLOLEDB.1; Integrated Security=SSPI" %("devmain1", "qamiscdb1")

####################################################################
## Setup
####################################################################

## connStrings: Map of Connection Strings -- name ==> connString        
mapDbnamesToConnstrings = {}
setConnStrings(mapDbnamesToConnstrings)
## conns: Map of Connections -- name ==> connection
conns = setupConnections(mapDbnamesToConnstrings)

dbData = {}

"""
For each DB:
    loop through all objects
    write one file: [dbname_objects_checksums.csv]
    store it in a dictionary by object-name
"""
for db, conn in conns.items():
    somgr = SysobjectMgr(dbname=db, conn=conn, rootDir = workDir)
    dbData[db] = somgr

"""
    ##     
    dbDataFn = getDbDataFileName(db)

    ## Load it or make a blank map
    mapObjects = unpickle(dbDataFn, {})
    
    mapObjects = getObjects(db, conn, mapObjects)
    pickle.dump(mapObjects, file(dbDataFn, "w"))
    for name, obj in mapObjects.items():
        print "%s => %s"%(name, obj)


"""
