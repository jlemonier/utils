from getxmlfromfilename import GetXmlFromFileName
from findtext import FindText

# csv file listing po & filename
# get xml
# find xpaths
# turn final csv into #tmp table
# run tp_findcity in loop -- same as for wsi

root = r"C:\GT\searsc"
fn_searsc_po_csv = root+r"\searsc_90days_po_all_intaudit_filename.csv"
fn_po_xpaths_list = root+r"\po_xpaths.list"

xpaths = []
for xp in file(fn_po_xpaths_list).readlines():
    xpaths.append(xp.strip())

if 2 < 1:
    print "-- Xpaths "
    for xp in xpaths:
        print "  %s"% (xp)

# om_po_id,pol_orig_city_id,pol_city_name,max_createtime,intaudit_id,filename,createtime
# 7349867,1002812,Manila,8/11/09 12:18 AM,865761479,\purchase_order\xml\imp860p_256_016005812.xml,8/11/09 12:18 AM
import csv
poReader = csv.DictReader(file(fn_searsc_po_csv))
i = 0

headers = []
for record in poReader:
    i = i + 1
    if i < -100:
        break
    # print row
    fn = record.get("filename", '')
    
    xmlText = GetXmlFromFileName(fn).mydata()

    ft = FindText(xmlText, xpaths, record)
    record2 = ft.getData()

    if len(headers) < 1:
        headers = record2.keys()
        headers.sort()
        print ",".join(headers)

    record3 = []
    for h in headers:
        v = record2.get(h, '')
        if v is None or v == "None":
            v = ""
        v = '"%s"'%(v)
        record3.append(v)

    print ",".join(record3)

    # if i < -100:
    #     print "\nFileName: %s ==> \nxml ==> %s \nrecord ==>%s "%(fn, xmlText, record)
