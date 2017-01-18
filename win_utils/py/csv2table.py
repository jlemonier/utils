######################################################################
# Purpose:
#   Take .csv file and produce a valid #tmp table for SQL Server
#
# Usage:
#  csv2table.bat data.csv
#   produces: data.csv.sql
#
# print statements in this file are written to %1.sql
######################################################################
import os, sys, csv, re

def write(line, fileObject = None):
    if fileObject is None:
        print (line)
    else:
        # print "%s\n"%(line)
        fileObject.write("%s\n"%(line))

def writeHeader(tableName, header, fileObject = None):
    line = "create table %s (\n\t  %s_id int identity(1,1) \n\t,%s \n) "%(tableName, tableName.replace("#",""), "\n\t,".join(map(dbCol, header)))
    write(line, fileObject)

def writeRow(tableName, header, row, fileObject = None):
    hcols = len(header)
    rcols = len(row)

    ## row = map(fixBadDq, row) --> no use here, must be against the whole line!

    if hcols != rcols:
        line = "-- Skipping -- cols in header=%s, cols in row=%s (insert fixed), data=%s -- "%(hcols, rcols, " | ".join(row))
        write (line, fileObject)
        for i in range(0, hcols-rcols):
            row.append("")
    else:
        row = row[0:hcols]
    ## Ensure # of elements in rows is same as in header
    line = "insert into %s (%s) values (%s) "%(tableName, ",".join(header), ",".join(map(quote, row)))
    write (line, fileObject)

## Fixing data such as My Product is 16", and 20' wide -- the ", kills some csv parsers.
bq = '(",)(?!")'
p = re.compile(bq)
def fixBadDq(s):
    s2 = p.sub("``,", s)  # finds:   ",16 and creates ``-16
    if len(s) != len(s2):
        print "-- fixed: %s"%(s2)
    s3 = s2.replace('","', '|')
    if s3[0] == '"':
        s3 = s3[1:]
    if s3[-1] == '"':
        s3 = s3[:-1]
    return s3

def quote(xstr, quoteChar="'"):
    if xstr.lower() == "null":
        return xstr
    else:
        xstr = xstr.replace("'","''")
        return quoteChar+xstr+quoteChar

def dbCol(col):
    col2 = col.lower()
    if col2.endswith("_id"):
        return " %s int" %(col)
    elif col2.endswith("time") or col2.endswith("created"):
        return " %s datetime " %(col)
    elif col2.find("active") >= 0:
        return " %s int " %(col)
    else:
        return " %s varchar(800) " %(col)

def fixHeaderCol(col):
    col = re.sub(r"[^a-zA-Z0-9_]", "", col)
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

def getOutputFile(fnIn, rows, rowsPerFile):
    if rowsPerFile <= 0:
        print "In getOutputFile: Defaulting to stdout. "
        return None    ## results in "print" statements and expected to be redirected

    # print "rows: %s rowsPerFile: %s"%(rows, rowsPerFile)
    counter = rows / rowsPerFile
    if counter < 1:
        fnOut = "%s.sql" %(fnIn)
    else:
        fnOut = "%s_%s.sql"%(fnIn, counter)
        
    print "-- Writing to %s ... "%(fnOut)
    return file(fnOut, "w")

def closeFile(fileObject):
    if fileObject is not None:
        fnOut.close()
        print "--     Closed file: %s "%(fnOut.name)

######################################################################

if len(sys.argv) < 2:
    print '-- No input file specified.'
    sys.exit()

## 2nd param is optional as table name.  defaults to #tmp
tableName = "#tmp"
if len(sys.argv) > 2:
    tableName = sys.argv[2]

delim = ","
quotechar = '"'
# 3rd param is optional for delim.  if |, pass "pipe"
if len(sys.argv) > 3:
    delim = sys.argv[3]
    if delim == "pipe":
        delim = "|"

print "Delim: %s"%(delim)

rowsPerFile = 50000  # if <= 0, then always %1.sql
preParse = False

"""

if len(sys.argv) > 3:
    rowsPerFile = int(sys.argv[3])
    if rowsPerFile < 1:
        print "3rd param for rowsPerFile was not an int"
        sys.exit()



if preParse:
    delim = "|"
    quotechar = None

"""

fnIn = sys.argv[1]  # fileName In
rows = 0

## fnOut == fileNameOut determined via function based on how many records have been written
fnOut = getOutputFile(fnIn, rows, rowsPerFile)

# print ("-- Processing %s now to produce a temp table %s for SQL Server"%(fnIn, tableName))
# print ("IF EXISTS (SELECT 1 FROM tempdb..sysobjects WHERE name LIKE '%s%%')"%(tableName))
# print ("   DROP TABLE %s "%(tableName))
line = "SET NOCOUNT ON"
write (line, fnOut)

## Playing with tricky csv files not quoted correctly
##  - preParse is False right now, so ignore
if preParse:
    ## PreParse the file and call fixBadDq on each line
    fnFix = fnIn+".fix"
    fout = file(fnFix, "w")
    pp = 0
    for line in file(fnIn).readlines():
        pp = pp + 1
        line = fixBadDq(line)
        if pp < 3:
            print line
        fout.write(line)
    fout.close()

    csvIn = fnFix
else:
    csvIn = fnIn

dataReader = csv.reader(file(csvIn), delimiter=delim, quotechar=quotechar)
# dataReader = csv.reader(file(csvIn), delimiter=delim)

header = []
i = 0

for row in dataReader:
    rows = rows + 1
    i = i + 1
    # print "read row %s => %s "%(i, row)

    ## Close & Create a new file now if batching output ...
    if rowsPerFile > 0 and i % rowsPerFile == 0:    
        closeFile(fnOut)
        fnOut = getOutputFile(fnIn, rows, rowsPerFile)
    
    # print row
    if len(header) < 1:
        header = row
        header = map(fixHeaderCol, header)       
        writeHeader(tableName, header, fnOut)
    else:
        writeRow(tableName, header, row, fnOut)

    if i % 50 == 0:
        print ("On record %s now ..."%(i))
        write ("print 'record: %s '"%(i), fnOut)
        write ("go", fnOut)
        write ("SET NOCOUNT ON", fnOut)

write ("select count(*) numRowsInTempTable, 'select top 10 * from #tmp' example_sql from %s "%(tableName), fnOut)
write ("select top 3 *, 'first3' first3 from %s order by 1      "%(tableName), fnOut)
write ("select top 3 *, 'last3'  last3  from %s order by 1 desc "%(tableName), fnOut)

write ("-- Created: %s insert statements into table: %s "%(rows, tableName))


closeFile(fnOut)
