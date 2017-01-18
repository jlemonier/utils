"""


select type, type_desc, count(*) from sys.objects group by type, type_desc order by type
==> devmain1
type	type_desc	(No column name)
C 	CHECK_CONSTRAINT	4
D 	DEFAULT_CONSTRAINT	4371
F 	FOREIGN_KEY_CONSTRAINT	3044
FN	SQL_SCALAR_FUNCTION	139
IF	SQL_INLINE_TABLE_VALUED_FUNCTION	7
IT	INTERNAL_TABLE	3
P 	SQL_STORED_PROCEDURE	2034
PK	PRIMARY_KEY_CONSTRAINT	1202
S 	SYSTEM_TABLE	41
SQ	SERVICE_QUEUE	3
TF	SQL_TABLE_VALUED_FUNCTION	13
TR	SQL_TRIGGER	13
U 	USER_TABLE	1614
UQ	UNIQUE_CONSTRAINT	15
V 	VIEW	131
"""

import time
import dbutils
import miscutils
import datetime
import threading
from miscutils import *
import pickle

def getSysobjectCols():
    return " name, type, type_desc, schema_id, modify_date "

## Sysobject class to store needed info
class Sysobject:

    ## Supports init with just a name
    def __init__(self, name, dbname = None, row = None, ):
        self.name = name        
        self.dbname = dbname or ""
        self.checksum = None
        self.lines = None
        
        if row is not None:
            self.setDataViaResultSet(row)
        
    def setDataViaResultSet(self, row):
        if row is not None and len(row) >= 5:
            self.name = row[0]
            self.type = row[1]
            self.type_desc = row[2]
            self.schema_id = row[3]
            self.modify_date = row[4]

    # For CSV header 
    def header(self):
        return "dbname | name | type | type_desc | lines | modify_date | checksum "
                        
    def __str__(self):
        return "%s | %s | %s | %s | %s | %s | %s"%(self.dbname, self.name, self.type, self.type_desc, self.lines, self.modify_date, self.checksum)

class SysobjectMgr (threading.Thread):
    def __init__(self, dbname, conn, exObjects = None, rootDir = r"c:\temp", debugTopX = None):
        ## Allow this program to work on many/all databases at the same time
        threading.Thread.__init__ ( self )

        self.dbname = dbname
        self.conn = conn
        self.rootDir = rootDir
        self.objects = {}
        self.exObjects = exObjects or {}
        self.debugTopX = debugTopX or 0     ## For Threading tests, we need this in constructor
        self.checkSumCalls = 0

        self.status = []                    ## Blank list


    def run(self):
        self.getSysObjects()

    def log(self, text):
        self.status.append(text)

    def printStatus(self):
        print "*** Status Messages for %s *** "%(self.dbname)
        for m in self.status:
            print m

    ## sp_helptext is what takes the most time
    ##  this function will handle comparing dates and deciding to do operation or not
    def setChecksum(self, name):
        chksum = None
        lines = None
        so = self.objects.get(name)     # sysobject
        sox = self.exObjects.get(name)  # sysobject existing
        if so and sox:
            if so.modify_date == sox.modify_date:
                # print " %s => new checksum: %s"%(name, so.checksum)
                # print " %s => old checksum: %s"%(name, sox.checksum)
                chksum = sox.checksum
                if hasattr(sox, 'lines'):
                    lines = sox.lines

        # Debug to force another call
        ## chksum = None

        if chksum is None:
            text = dbutils.sp_helptext(name, self.conn)
            if text is not None:
                lines = len(text.split("\n"))
            chksum = dbutils.checkSum(text)
            self.checkSumCalls = self.checkSumCalls + 1
            if self.checkSumCalls % 50 == 0:
                self.log( " ... %sth call to sp_helptext on %s "%(self.checkSumCalls, name))

        ## Must not indent this.  Either from cache or new call, set checksum
        so.checksum = chksum
        so.lines = lines

    ## Get single record of data from sys.objects and produce object
    def getSysObject(self, name, row = None):
        if row is None:
            conn = self.conn
            cols = getSysobjectCols()
            sql = "select %s from sys.objects where name = '%s' " %(cols, name)
            rows = dbutils.getRows(conn, sql)      
            if len(rows) == 1:
                row = rows[0]
        if row is None:
            row = []

        so = Sysobject(name, self.dbname, row)
        self.objects[name] = so
        self.setChecksum(name)
        
        return so

    ## mapObjects passed in which may be blank OR it may have serialized results from previous run
    ##  - We want to skip the "sp_helptext" on 1000's of objects if the 
    ## Adds object=>modified to dbobjects Map (dictionary)
    def getSysObjects(self, debugTopX = None):
        self.status = []
        debugTopX = debugTopX or self.debugTopX or 0
        # print "In SysobjectMgr.getSysobjects for db: %s debugTopX: %s"%(self.dbname, debugTopX)
        self.checkSumCalls = 0
        start = time.time()
        debugFnPart = ""   # Blank if no debugging
        if debugTopX > 0:
            debugFnPart = ".testTop%s"%(debugTopX)
        fnCache = os.path.join(self.rootDir, "%s%s.pickle.bin"%(self.dbname, debugFnPart))
        fnCsv = os.path.join(self.rootDir, "%s%s.csv"%(self.dbname, debugFnPart))
        fCsv = file(fnCsv, "w")
        
        self.exObjects = miscutils.unpickle2(fnCache, {})

        maxDateModified = datetime.datetime(1980, 1,1)
        for so in self.exObjects.values():
            somd = so.modify_date
            if somd > maxDateModified:
                maxDateModified = somd
        self.log("Max Date Modified for DB %s => %s "%(self.dbname, maxDateModified))
        
        ## Enable the sql to be passed in
        cols = getSysobjectCols()
        # sql = "select %s from sys.objects where type in ('FN','IF','P','TF', 'X', 'RF', 'FS', 'FT') and modify_date >= '%s' " %(cols, maxDateModified.strftime("%Y-%m-%d %H:%M:%S"))
        sql = "select %s from sys.objects where type in ('FN','IF','P','TF', 'X', 'RF', 'FS', 'FT') " %(cols)
        
        ## Test SQL
        if debugTopX > 0:
            # print "DEBUGGING in sysobject.py only %s objects"%(debugTopX)
            sql = "select top %s %s from sys.objects where type in ('V') order by name desc" %(debugTopX, cols)

        # rows = getRows(conn, sql) ## N
        # print sql
        start = time.time()
        curs = self.conn.cursor()
        curs.execute(sql)
        rows = curs.fetchall()
        """ for d in curs.description: print repr(d) """
        end = time.time()
        self.log("Returned %s rows in %.3f seconds via SQL: %s"%(len(rows), end-start, sql))
        
        for row in rows:
            objname = row[0]
            self.objects[objname] = self.getSysObject(objname, row)

        ## Write out binary & csv (csv for reference only)
        miscutils.pickle2(self.objects, fnCache)
        for o in self.objects.values():
            fCsv.write("%s\n"%(o))
        fCsv.close()

        ## Printing ... 
        i = 0
        for name, so in self.objects.items():
            i = i + 1
            if i % 100 == 0 or i <= 10:
                self.status.append("%s) %s"%(i, so))

        end = time.time()
        elapsed = end-start
        perCall = 0
        if self.checkSumCalls > 0:
            perCall = elapsed / self.checkSumCalls
        self.log("\n\nCalled sp_helptext %s times over %s objects.  Took %.2f seconds.  %.2f per call. \n\n"%(self.checkSumCalls, len(self.objects), end-start, perCall))
                
        return self.objects


############################################################################################################
## sysobject module functions used to create one-or-more Sysobject classes correctly
############################################################################################################    

def testMe():
    dbname,dbserver = "devmain1","qamiscdb1"
    name = "tp_daily_stats"
    qamain1ConnString = r"Initial Catalog=%s; Data Source=%s; Provider=SQLOLEDB.1; Integrated Security=SSPI" %(dbname , dbserver)
    rootDir = r"c:\temp"

    conn = dbutils.getConn(qamain1ConnString)

    somgr = SysobjectMgr(dbname=dbname, conn=conn, rootDir=rootDir)

    testObjects = somgr.getSysObjects(50)
    somgr.printStatus()
    testObjects = somgr.getSysObjects(100)
    somgr.printStatus()

    testThread = False
    # if testThread:  

def mySleep(seconds, msg=""):
    print "Sleeping for %s seconds.  %s"%(seconds, msg)
    time.sleep(30)
    print "Done Sleeping for %s seconds.  %s"%(seconds, msg)
  
"""   
# testMe()

dbname,dbserver = "devmain1","qamiscdb1"
name = "tp_daily_stats"
qamain1ConnString = r"Initial Catalog=%s; Data Source=%s; Provider=SQLOLEDB.1; Integrated Security=SSPI" %(dbname , dbserver)
rootDir = r"c:\temp"

conn = dbutils.getConn(qamain1ConnString)

t1 = SysobjectMgr(dbname=dbname, conn=conn, rootDir=rootDir, debugTopX=151)
t1.start()
t1.join()

# mySleep(30)

"""