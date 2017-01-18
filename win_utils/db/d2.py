from dbutils import *
from tables import Tables

myTables = Tables()
## myTables.testPrintTable()

dbInfo = {}
dbServer = 'qamaindb1'
dbInfo['qamain1'] = dbServer

connStrings = {}
for db,server in dbInfo.iteritems():        
    connStrings[db] = r"Initial Catalog=%s; Data Source=%s; Provider=SQLOLEDB.1; Integrated Security=SSPI" %(db , server)
    
connStrings["newtradmarket"] = "DSN=pnetdb1a;  Uid=engdbread; Pwd=(^P1t^!s$"

srcConn = getConn(connStrings['qamain1'])
# rows = getRows2(srcConn, sql, cols)

cols = {}
sql = "select top 1 * from tt_om_po order by 1 desc"
rs = getResultSet(srcConn, sql)
while rs.next():
    col = "om_po_id"
    print "%s => %s"%(col, rs.get(col))


print "# rows=%s, # cols=%s"%(rs.getNumRows(),len(rs.getCols()))



