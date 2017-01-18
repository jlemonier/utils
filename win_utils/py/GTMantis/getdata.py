## Python Script to generate data repair sql script for BugID: 49369

# 1) read csv data with these columns: ponum,om_po_id,tag_id,tag_val,filename,controlnum,editime
#      Example data rows:
#       973898,7835567,NULL,NULL,\purchase_order\xml\imp850p_343.edi_016000384.xml,16000384,08:00.0
#       973723,7822864,NULL,NULL,\purchase_order\xml\imp850p_215.edi_016000010.xml,16000010,09:00.0
#
#       \purchase_order\xml\imp850p_343.edi_016000384.xml is from tt_intaudit.filename

# 2) strip path of filename to get: imp850p_343.edi_016000384.xml

# 3) a) http post to pfile1a: http://pfile1a/file_search_results.asp?EnvironmentType=prod&MessageType=orders&FileNameValue=imp850p_115.edi_016000115.xml
#    b) retrieve data: |1|imp850p_551.edi_016000387.xml| http://pfile1a/prodinboundbackup\20090708\orders\po\xml\searscanada\imp850p_551.edi_016000387.xml| http://pfile1a| size 31281 bytes| 7/8/2009 11:10:30 PM GMT|*|
#    

# 4) retrieves xml text from http://pfile1a/prodinboundbackup\20090708\orders\po\xml\searscanada\imp850p_551.edi_016000387.xml

# 5) parses xml text using xml xpath to: "Order/Header/Tags/Tag/Value"

# 6) generate sql to run to add this tag:
#    -- PONum: 968936 om_po_id: 7640854 file: searscanada\imp850p_115.edi_016000115.xml xmlUrl: http://pfile1a/prodinboundbackup\20090408\orders\po\xml\searscanada\imp850p_115.edi_016000115.xml POSystem: SMARTIMP 
#    exec tp_save_tag 'SMARTIMP', 'POSystem', 60001, 7640854, 35540

# 7) Show SQL clause 




import os, sys
from os import path

import urllib2
import xml.etree.ElementTree as ET # Python 2.5

debug = 1

failedPoNum = []
failedId = []

okId = []
   

def getDataFromUrl(url):
    f = urllib2.urlopen(url)
    data = f.read()
    return data

def removeHtmlHeader(data):
    i = data.find("</HEAD>")+8
    # print i
    d2 = data[i:]
    # print "... <HEAD/> removed: %s" %d2
    return d2

# http://pfile1a/file_search_results.asp?EnvironmentType=prod&MessageType=orders&FileNameValue=imp850p_115.edi_016000115.xml
def getFileJockeyPath(fn):
    preurl = "http://pfile1a/file_search_results.asp?EnvironmentType=prod&MessageType=orders&FileNameValue=%s" %(fn)
    # print "trying url: %s" %(preurl)
    metadata = getDataFromUrl(preurl)
    metadata2 = removeHtmlHeader(metadata)
    m1cols = metadata2.split("|")
    dataurl = m1cols[3].strip()
    # print "data url: %s"%dataurl
    return dataurl

    #url = r"http://pfile1a/prodinboundbackup\20090408\orders\po\xml\searscanada\imp850p_115.edi_016000115.xml"
    # url = url.replace(r"\\", "/")
    # return url

def getDataForXpath(xmltree, xpath):
    try:
      return xmltree.findtext(xpath)
    except:
        rc = ''
    if rc is None:
        rc = ''
    return rc

def evalRow(po, om_po_id, fn):
    try:
        fnbase = os.path.basename(fn)
        # print "filename base: %s"%fnbase
        fjp = getFileJockeyPath(fnbase)
        xmldata = getDataFromUrl(fjp)
        # print xmldata[:100]

        # xmltree = ET.parse(xmldata)
        xmltree = ET.fromstring(xmldata)
        posystem = getDataForXpath(xmltree, "Order/Header/Tags/Tag/Value")
        print "\n-- PONum: %s om_po_id: %s file: %s xmlUrl: %s POSystem: %s "%(po, om_po_id, fn, fjp, posystem)
        tp_save_tag = """
        create procedure dbo.tp_save_tag
	@tag_value				varchar(255),
	@tag_type				varchar(255),
	@tagged_object_type_id	int,	-- cm, po, etc. from tz_objtype
	@tagged_object_id		int,	-- fk value to om_po_id, om_cm_id, etc
	@org_id					int 	-- org id this tag belongs to
	"""

        print "exec tp_save_tag '%s', '%s', %s, %s, %s" %(posystem, 'POSystem', '60001', om_po_id, 35540)

        okId.append(om_po_id)
    except:
        print "\n-- failed for ponum=%s om_po_id=%s file=%s" %(po, om_po_id, fn)

        failedPoNum.append("'%s'"%po)
        failedId.append(om_po_id)


inputfile = "49369_po_creates.csv" 
fin = file(inputfile)
hdr = fin.readline()
print "-- Input file: %s "%(inputfile)
print "-- Header line of input file: %s"%hdr

i = 0

for line in fin.readlines():
    i = i + 1
    
    line = line.strip()
    cols = line.split(",")

    po = cols[0]
    om_po_id = cols[1]
    fn = cols[4]
    
    if len(fn) > 0:
        evalRow(po, om_po_id, fn)

print "\n\n/* -- Printing failed om_po_id and ponum as sql where the POSystem could not be found (perhaps in last 2 days only"
print " failed: om_po_id in ( %s ) " %(",".join(failedId))
print " failed: ponum in ( %s ) " %(",".join(failedPoNum))
print " success: om_po_id in ( %s ) " % (",".join(okId))
print "*/ "
