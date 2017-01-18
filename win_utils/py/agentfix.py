## Bug 60122=CostPlus, 60275=Warnaco, 
## Get CostPlus PO #s & mssg_doc_id.
## Get each PO_ponum123_mssgdocid8787.xml
## xpath to agent: code, name
## datafix

import os
import sys
import pickle
import traceback
## Organizing code, putting functions in dbutils.py and miscutils.py modules
import dbutils
from dbutils import *
from miscutils import *
import xml.etree.ElementTree as ET # Python 2.5

org_id = 12648   # SHC
orgname = "wsi"
findPartyTypes = ["Agent"]

poSql = """

select 
	
	po.ponum, po.om_po_id, po.modtime, max(ia.createtime) ia_createtime_max
	, datediff(mi, po.modtime, max(ia.createtime)) delta_poMod_iaMod
	, max(ia.intaudit_id) intaudit_id
	, max(ia.mssgdoc_id)  mssgdoc_id

	-- , max(ia2.createtime) createtime_mostrecent
	-- , max(ia2.mssgdoc_id) mssgdoc_id_mostrecent
	from		tt_intaudit ia								-- with(index (tt_intaudit_createtime_cx1)) -- broke PoParty

	inner join	tt_om_po po on po.om_po_id = ia.gtn_id
/*
	left loop join	tt_intaudit ia2
					on  ia2.gtn_id = po.om_po_id
					and ia2.msgid = '850'
					and ia2.msgdirection = 'IN'
*/
	where ia.createtime > '2010-07-02 16:00'
	and   ia.createtime < '2010-07-09 09:00'
	and   ia.msgid = '850'
	and   ia.msgdirection = 'IN'
	and   ia.severity < 3
	and   ia.primary_org_id in (%s)
	-- and   msgtype = 'XML'

	and po.customer_org_id = %s
	and po.modtime between '2010-07-02 16:00' and '2010-07-09 09:00'
	
        -- and po.ponum in ('B53CT')

    group by po.ponum, po.om_po_id, po.modtime
	order by po.ponum


/*
controlnum
createtime, msgid, msgdirection, severity, gtn_id, controlnum
gtn_id, refid, msgid, msgdirection, severity
msgid, msgdirection, severity, createtime, gtn_id, refid, controlnum
intaudit_id
*/

""" %(org_id, org_id)


def setConnStrings(connStrings = None):
    if connStrings is None:
        connStrings = {}
    connStrings["newtradmarket"] = "DSN=pnetdb1a;  Uid=engdbread; Pwd=(^P1t^!s$"
    connStrings["newtradmarket2"] = "DSN=pnetdb1a;  Uid=engdbread; Pwd=(^P1t^!s$"
    connStrings["newtradmarket_reporting_daily"] = r"Initial Catalog=%s; Data Source=%s; Provider=SQLOLEDB.1; Integrated Security=SSPI" %("newtradmarket_reporting_daily", "pdb1a")
    connStrings["mssg"] = r"Initial Catalog=%s; Data Source=%s; Provider=SQLOLEDB.1; Integrated Security=SSPI" %("mssg_newtradmarket", "pdb1a")
    return connStrings

def getXml(mssgdoc_id):
    conn = conns['mssg']
    sql = "select document from tt_mssg_doc where mssg_doc_id = %s"%(mssgdoc_id)
    rows = dbutils.getRows(conn, sql)
    xml = "?"
    if len(rows) > 0:
        xml = rows[0][0]
    return xml

def getColumn(colName, row, colNames):
    i = None
    if colNames.has_key(colName):
        i = colNames[colName]
    if i is not None and len(row) > i-1:
        return row[i]

def getOrgForCode(code, conn):
    # conn = getConn(connStr)
    sql = "select max(org_id) org_id, code, count(distinct org_id) num_orgs from tt_om_partner p where p.ref_org_id = 2119 and partner_type=11 and code = '%s' and isactive = 1 group by code "%(code)
    # sql = "select top 1 org_id, code from tt_om_partner"
    # print sql
    rows = dbutils.getRows(conn, sql)
    # print rows
    if len(rows) == 1:
        row = rows[0]
        org_id = row[0]
        return org_id
    return 0

def write(msg, fOut, rowNum = 1):
    if rowNum % 100 == 0 or rowNum < 10:
        print msg
    fOut.write("%s\n"%(msg))

def getXmlCache(mssgdoc_id, fileName, debug = False, rowNum = 1):
    if rowNum > 10:
        debug = False
        
    if rowNum % 100 == 0 or rowNum < 10:
        debug = True
        
    xml = ""
    if os.path.exists(fileName):
        if debug:
            print "%s) File %s exists already, getting contents"%(rowNum, fileName)
        xml = file(fileName).read()
        if len(xml) > 20:
            return xml
        else:
            print "%s) File %s exists already, but there were no contents."%(rowNum, fileName)
        # return ""

    if debug:
        print "%s) File %s does not exist.  Getting xml from mssgdoc_id=%s and caching it."%(rowNum, fileName, mssgdoc_id)
    xml = getXml(mssgdoc_id)
    try:
        fOut = file(fileName, "w")
        fOut.write(xml)
        fOut.close()
    except Exception, e:
        print "Failed writing file %s - mssgdoc_id=%s "%(fileName, mssgdoc_id)
        print e
        print sys.exc_info()[0]
        
    return xml

def printEx ():
    # for se in sys.exc_info():
    #        print "   %s => %s"%(type(se), str(se))
    traceback.print_exc()

mapDbnamesToConnstrings = {}
setConnStrings(mapDbnamesToConnstrings)
## conns: Map of Connections -- name ==> connection
conns = setupConnections(mapDbnamesToConnstrings)

##  connTm = conns['newtradmarket_reporting_daily']
connTm = conns['newtradmarket']
connTm2 = conns['newtradmarket2']
connMS = conns['mssg']

conn = connTm
sql = poSql

print sql

# rows = dbutils.getRows(connNewtm, sqlCostplus)
curs = conn.cursor()
curs.execute(sql)
rows = curs.fetchall()

print "Found %s rows"%(len(rows))

colNames = {}

r1 = rows[0]

iCol = -1
for d in curs.description:
    iCol = iCol +1
    colNames[d[0]] = iCol

# print dir(r1)
#for c,i in colNames.items():
#   print c, i

xpaths = []
xpaths.append('Order/Header/PartyInfo')
# xpaths.append('Order/Header/PartyInfo[1]/Code')

cpOut = file("%s_agent_fix.csv"%(orgname), "w")

## print Header
write( "ponum|om_po_id|intaudit_id|mssgdoc_id|partytype|code|name|org_id|filename", cpOut)

numPerType = {}
rowNum = 0

xmlDir = "xml_%s"%(orgname)
if not os.path.isdir(xmlDir):
    os.makedirs(xmlDir)

for r in rows:
    rowNum = rowNum + 1
    
    ponum = getColumn('ponum', r, colNames)
    om_po_id = getColumn('om_po_id', r, colNames)
    mssgdoc_id = getColumn('mssgdoc_id', r, colNames)
    intaudit_id = getColumn('intaudit_id', r, colNames)

    fName = r"%s\POnum-%s_MssgDocId-%s.xml"%(xmlDir, ponum, mssgdoc_id)

    print "%s) file: %s"%(rowNum, fName)
    
    xml = getXmlCache(mssgdoc_id, fName, True, rowNum)

    try:
        xmlTree = ET.fromstring(xml)

        for node1 in xmlTree:
            if node1.tag == "Order":
                for node2 in node1:
                    if node2.tag == "Header":
                        for hdrnode in node2:
                            if hdrnode.tag == "PartyInfo":
                                party = hdrnode

                                partyType = party.findtext("Type")
                                if partyType in findPartyTypes:
                                # if party.findtext("Type") == findPartyType:
                                    # numAgents = numAgents + 1
                                    numPerType[partyType] = numPerType.get(partyType, 0) + 1
                                    agentCode = party.findtext("Code")
                                    agentName = party.findtext("Name")
                                    
                                    ## pt_org_id = getOrgForCode(agentCode, connTm2)
                                    pt_org_id = 0
                                    # print "PONum|%s|Agent|%s|Type|%s|Code|%s|pt_org_id|%s|filename|%s" %(ponum, party, party.findtext("Type"), agentCode, pt_org_id, fName)
                                    write( "%s|%s|%s|%s|%s|%s|%s|%s|%s" %(ponum, om_po_id, intaudit_id, mssgdoc_id, partyType, agentCode, agentName, pt_org_id, fName), cpOut, rowNum)

    except Exception, e:
        print "Failed parsing file: %s "%(fName)
        print e
        printEx()

for ptype,num in numPerType.items():
    print "\n\n Type: %s  #-for-type: %s  Total-Rows: %s"%(ptype, num, len(rows))

cpOut.close()
