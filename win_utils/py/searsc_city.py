from getxmlfromfilename import GetXmlFromFileName
from findtext import FindText
import csv
import sys
import os

# csv file listing po & filename
# get xml
# find xpaths
# turn final csv into #tmp table
# run tp_findcity in loop -- same as for wsi

root = r"C:\GT\searsc\city"
# fn_searsc_po_csv = root+r"\searsc_90days_po_all_intaudit_filename.csv"
# fn_searsc_po_csv = root+r"\sears200.csv"
fn_searsc_po_csv = root+r"\sears_add_po_8330.csv"

fn_po_xpaths_list = root+r"\po_xpaths.list"

xpaths = []
for xp in file(fn_po_xpaths_list).readlines():
    xp = xp.strip()
    xpaths.append(xp)
    # print "%s"%(xp)

if 2 < 1:
    print "-- Xpaths "
    for xp in xpaths:
        print "  %s"% (xp)

# om_po_id,pol_orig_city_id,pol_city_name,max_createtime,intaudit_id,filename,createtime
# 7349867,1002812,Manila,8/11/09 12:18 AM,865761479,\purchase_order\xml\imp860p_256_016005812.xml,8/11/09 12:18 AM
poReader = csv.DictReader(file(fn_searsc_po_csv))

fnOut = fn_searsc_po_csv+".out"
fOut = file(fnOut, "w")

def write(msg, i):
    x = 50
    fOut.write(msg + "\n")
    if i < 10:
        print (msg)
    elif i == 10:
        print "--- Printing every %s records now to output only ... "%(x)
    elif i % x == 0:        
        print ("%s ==> %s"%(i, msg))


            
i = 0
headers = []
for record in poReader:
    i = i + 1
    # if i > 10: break
    
    # print row
    fn = record.get("filename", '')

    ## Try to find xml file in local xml directory
    xmlText = ""
    try:
        fn2 = os.path.basename(fn)
        fnLocal = r".\\xml\\%s"%(fn2)
        if os.path.exists(fnLocal):
            xmlText = file(fnLocal).read()
    except:
        xmlText = ""

    if len(xmlText) < 1:
        xmlText = GetXmlFromFileName(fn).mydata()

        try:
            xmlOut = file(r".\\xml\\%s"%(os.path.basename(fn)), "w")
            xmlOut.write(xmlText)
            xmlOut.close()
            # print "Wrote xml file: %s"%(fn)
        except:
            print "Failed to write xml file: %s ==> %s "%(fn, sys.exc_info())

    else:
        print "Cached xml file %s found in xml directory"%(fnLocal)

    ft = FindText(xmlText, xpaths, record)
    record2 = ft.getData()

    if i < -300:
        ## print "record2: %s ==> %s "%(i, record2.keys())
        print "record2 keys: "
        r2keys = record2.keys()
        r2keys.sort()
        for k in r2keys:
            print "  %s in record: %s"%(k, i)
        print "record2: %s ==> %s "%(i, record2)

    if len(headers) < 1:
        headers = record2.keys()
        headers.sort()
        write (",".join(headers), i)

    record3 = []
    for h in headers:
        v = record2.get(h, '')
        if v is None or v == "None":
            v = ""
        v = v.replace('"', '')      # no " in the data
        v = '"%s"'%(v)
        record3.append(v)

    write (",".join(record3), i)

    # if i < -100:
    #     print "\nFileName: %s ==> \nxml ==> %s \nrecord ==>%s "%(fn, xmlText, record)

fOut.close()

print "---> %s just created. "%(fnOut)
