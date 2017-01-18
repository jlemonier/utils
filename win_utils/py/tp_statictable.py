
import os, sys, csv, re

## 2nd param is optional as table name.  defaults to #tmp
tableName = "#tmp"
if len(sys.argv) > 2:
    tableName = sys.argv[2]

fnIn = r"C:\GT\Bugs\intaudit_msgid.csv"
if len(sys.argv) > 1:
    fnIn = sys.argv[1]

fIn = file(fnIn)

strcols = [2,3,4]

fOut = file("%s.out"%(fnIn), "w")

# exec tp_statictable_add 'tz_intaudit_msgid', @cols, '4,  4,  ''304'',        ''EDI'',        ''IN'',  1';
for line in fIn.readlines():
    line = line.strip()
    record = line.split(",")
    # print record

    for coli in range(2,5):
        record[coli] = "''%s''" %(record[coli])

    line2 = "exec tp_statictable_add 'tz_intaudit_msgid', @cols, '%s';"%(", ".join(record))
    print line2
    fOut.write(line2 + "\n")


fOut.close()
