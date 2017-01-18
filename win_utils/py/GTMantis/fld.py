fin = file("fields.txt")
sql = " select "
for line in fin.readlines():
    line = line.strip()
    pos,fld = line.split("\t")
    ipos = int(pos) - 1
    sql = sql + "\n d%s as '%s', "%(ipos, fld)
print sql
