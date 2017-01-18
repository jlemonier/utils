######################################################################
# Purpose:
#   Take .csv file and produce a valid #tmp table for SQL Server
#
# Usage:
#  csv2table.bat data.csv
#   produces: data.csv.sql
######################################################################
import os, sys, csv, re

def writeHeader(tableName, header):
    print ("create table %s (\n\t  %s_id int identity(1,1) \n\t,%s \n) "%(tableName, tableName.replace("#",""), "\n\t,".join(map(dbCol, header))))

def writeRow(tableName, header, row):
    hcols = len(header)
    rcols = len(row)

    if hcols != rcols:
        print ("-- cols in header=%s, cols in row=%s (insert fixed), data=%s -- "%(hcols, rcols, ",".join(row)))

    for i in range(0, hcols-rcols):
        row.append("")
    row = row[0:hcols]

    ## Ensure # of elements in rows is same as in header
    print ("insert into %s (%s) values (%s) "%(tableName, ",".join(header), ",".join(map(quote, row))))

def quote(xstr, quoteChar="'"):
    xstr = xstr.replace("'","''")
    return quoteChar+xstr+quoteChar

def dbCol(col):
    col2 = col.lower()
    if col2.endswith("_id"):
        return " %s int" %(col)
    elif col2.endswith("time") or col2.endswith("created"):
        return " %s datetime " %(col)
    else:
        return " %s varchar(800) " %(col)

def fixHeaderCol(col):
    col = re.sub(r"[^a-zA-Z0-9]", "", col)
    col = col.replace("PortOfLoading","POL")
    col = col.replace("PortOfDischarge","POD")
    col = col.replace("Origin", "Orig")
    col = col.replace("CityCity", "City")
    col = col.replace("Transaction", "Tran")
    col = col.replace("Destination", "Dest")
    col = col.replace("Message", "Msg")
    col = col.replace("ASN","Asn")
    col = col.replace("Qualifier","Qual")
    return col

######################################################################

if len(sys.argv) < 2:
    print '-- No input file specified.'
    sys.exit()

tableName = "#tmp"
if len(sys.argv) > 2:
    tableName = sys.argv[2]

fnIn = sys.argv[1]  # fileName In
fIn = file(fnIn)    # file In
fnIn = file(sys.argv[1])
print ("-- Processing %s now to produce a temp table %s for SQL Server"%(fnIn, tableName))
print ("IF EXISTS (SELECT 1 FROM tempdb..sysobjects WHERE name LIKE '%s%%')"%(tableName))
print ("   DROP TABLE %s "%(tableName))
print ("SET NOCOUNT ON")
dataReader = csv.reader(fnIn, delimiter=',', quotechar='"')
header = []
i = 0

for row in dataReader:
    i = i + 1
    # print row
    if len(header) < 1:
        header = row
        header = map(fixHeaderCol, header)
        
        writeHeader(tableName, header)
    else:
        writeRow(tableName, header, row)

    if i % 100 == 0:
        print "go"


print ("select count(*) numRowsInTempTable, 'select top 10 * from #tmp' example_sql from %s "%(tableName))
print ("select top 3 *, 'first3' first3 from %s order by 1      "%(tableName))
print ("select top 3 *, 'last3'  last3  from %s order by 1 desc "%(tableName))


