import os, sys, csv

tableName = "#tmp_prod"

fnIn = "msft_v4.csv"
fnOut = "load.sql"

fin = csv.reader(open(fnIn), delimiter=',', quotechar='"')
fout = file(fnOut, "w")

def isNumeric(type):
    return type.find("char") < 0

def sqlWrap(data, isNum):
    if isNum:
        if len(data) < 1:
            return 'null'
        return data
    else:
        return "'%s'"%(data)

def genInsert(tableName, row, colName, colType):
    values = []
    i = 0
    for col in colName:
        i = i+1
        t = colType[col]
        isNum = isNumeric(t)
        # print ("%s -- %s"%(i, col))
        values.append(sqlWrap(row[i-1], isNum))
        
    sql = "insert into %s (%s) values (%s)" %(tableName, ", ".join(colName), ", ".join(values))
    return sql
    


colDefs = """
          code varchar(255)
	, name varchar(255)
	, standard_masterpack_qty float
	, product_category_1 varchar(255)
	, unitvolume float
	, unitweight float
	, product_category_2 varchar(255)
	, product_category_3 varchar(255)
"""

colList = colDefs.split(",")
colName = []
colType = {}
for c in colList:
    c = c.strip()
    # print (c)
    if len(c) > 0:
        col,ctype = c.split(" ", 1)
        colType[col] = ctype
        colName.append(col)

# Print the columns
j = 0
for c in colName:
    j = j +1
    t = colType[c]
    isn = isNumeric(t)
    print ("%s = %s of type: %s -> numeric=%s"%(j, c, t, isn))

fout.write("\ndrop table %s \n"%(tableName))
fout.write("create table %s ( id int identity(1,1), %s ) "%(tableName, colDefs))

i = 0
rows = 0
for row in fin:
    i = i + 1
    if i < 2:
        continue
    sqlIns = genInsert(tableName, row, colName, colType)
    fout.write("\n"+ sqlIns)
    rows = rows + 1
    if i < 5:
        print (row)
        print (sqlIns)

fout.write ("\n\nselect count(*) as rows_in_%s from %s " %(tableName, tableName))
# fin.close()
fout.close()
