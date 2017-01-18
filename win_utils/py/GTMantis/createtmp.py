import os

fn = "cpwm_po_tags.txt"
fnout = "cptag.sql"

fin = file(fn)
fout = file(fnout, "w")

def div3(div):
    rc = "000" + div
    return rc[-3:]

i = 0

for line in fin.readlines():
    line = line.strip()
    parts = line.split("\t")
    if len(parts) >= 3:
        i = i +1
        po, old, new = parts
        old = div3(old)
        new = div3(new)
        sql = "insert into #cptag (ponum, divold, divnew) values ('%s','%s','%s') " %(po, old,new)
        fout.write(sql + "\n")

print "Created %s insert statements in %s" %(i, fnout)
fin.close()
fout.close()
    
