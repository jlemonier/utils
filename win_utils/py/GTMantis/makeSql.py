import os, sys

fin = file("47416_po_agent2.csv")

T = "'"

def tic(s):
  return T+s+T

print "create table #tmp ( oldcode varchar(50), oldname varchar(255), ponum varchar(255), newcode varchar(50), newname varchar(255) ) "

i = 0
for line in fin.readlines():
    i = i + 1
    if i == 1:
        continue
    line = line.strip()
    # print line
    flds = line.split(",")
    
    cols = "oldcode, oldname, ponum, newcode, newname"
    if len(flds) >= 5 and len(flds[0]) > 0:
      print "insert into #tmp (%s) values (%s) "%(cols, ",".join(map(tic, flds[:5])))
    else:
      print "-- line did not create insert statement! %s"%(line)
