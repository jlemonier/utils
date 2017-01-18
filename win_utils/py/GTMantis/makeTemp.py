import sys
import getopt

def wrap(s):
    return "'%s'"%(s)

inputFile = "input.csv"
tableName = "#tmp"
delim = ","

argv = sys.argv
if len(argv) > 1:
    inputFile = argv[1]
if len(argv) > 2:
    tableName = argv[2]
if len(argv) > 3:
    delim = argv[3]

fin = file(inputFile)

header = fin.readline()
header = header.strip()
cols = header.split(",")

def createTable(tableName):
    coldefs = []
    for c in cols:
        coldefs.append("%s varchar(50) "%(c))
        
    sql = "create table #tmp ( %s ) " %(",".join(coldefs))
    return sql

createTmpSql = createTable(tableName)

print "set nocount on"

print createTmpSql
i = 0
bad = 0

records = []
for line in fin.readlines():
    i = i + 1
    if i > 999999:
        break
    line = line.strip()
    cells = line.split(delim)[:len(cols)]           # create cells with 1-> 5+ columns

    # if cells[0].startswith("CK"):
    #    continue

    ## wow, this is huge!!  2400 records kept working for 25+ minutes on qalive1.
    ## now it is 12 seconds!
    if i % 100 == 0:
        print "go"
    
    cells[:] = [x for x in cells if x is not None]  # remove blank
    for xx in range(1, 3):                          # ensure 3+ columns exist
        cells.append ('')
    cells = cells[:3]                               # trim list to 3
    cells = map(wrap, cells)                        # wrap all with '
    if len(cells) != 3:
        bad = bad + 1
    records.append(",".join(cells))
    print "insert into %s (%s) values (%s)"%(tableName, ",".join(cols), ",".join(cells))
    # print "select %s union all "%(",".join(cells))

# print " unionall \n".join(records)
print "-- bad=%s"%(bad)
