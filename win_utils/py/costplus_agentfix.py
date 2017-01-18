## Bug 60122
## Get CostPlus PO #s & mssg_doc_id.
## Get each PO_ponum123_mssgdocid8787.xml
## xpath to agent: code, name
## datafix

import os
import sys
import pickle
## Organizing code, putting functions in dbutils.py and miscutils.py modules
import dbutils
from dbutils import *
from miscutils import *

import xml.etree.ElementTree as ET # Python 2.5

sqlCostplus = """

-- declare @org_id int; select @org_id = 3760
select
	-- datepart(month, ia.createtime) month, datepart(day, ia.createtime) day
	-- max(ia.createtime) ia_createtime, max(po.modtime) po_modtime
	po.ponum, po.om_po_id, po.modtime, ia.intaudit_id
	, max(ia.mssgdoc_id) mssgdoc_id
	-- , pop.org_id STAMP_pop_org_id, pop.code, pop.name, pop.email_address, pop.isactive 
	-- , refname, primary_org_id, severity, reasontext
	-- , substring ( reasontext, charindex('[', reasontext)+1, charindex(']', reasontext)-1 - charindex('[', reasontext) )
	-- , p.code, p.org_id
	from tt_intaudit ia

	left join tt_om_po po on po.ponum = ia.refname and po.customer_org_id = 3760 and po.isactive = 1
/* -- blue heron
	left join tt_om_partner p 
		on  p.email_address = substring ( reasontext, charindex('[', reasontext)+1, charindex(']', reasontext)-1 - charindex('[', reasontext) )
		and p.ref_org_id    = 3760
		and p.ref_orgdiv_id = po.customer_orgdiv_id
	*/
	left join tt_om_poparty pop
		on  pop.om_po_id = po.om_po_id
		and pop.om_partytype_id = 11
		and pop.isactive        = 1
	
	where ia.createtime > '2010-07-01'
	and   msgid = '850'
	and   msgdirection = 'IN'
	and   severity = 2
	and   primary_org_id = 3760
        group by po.ponum, po.om_po_id, po.modtime, ia.intaudit_id

	order by po.modtime desc

"""


def setConnStrings(connStrings = None):
    if connStrings is None:
        connStrings = {}
    connStrings["newtradmarket"] = "DSN=pnetdb1a;  Uid=engdbread; Pwd=(^P1t^!s$"
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
    sql = "select max(org_id) org_id, code, count(distinct org_id) num_orgs from tt_om_partner p where p.ref_org_id = 3760 and partner_type=11 and code = '%s' and isactive = 1 group by code "%(code)
    # sql = "select top 1 org_id, code from tt_om_partner"
    # print sql
    rows = dbutils.getRows(conn, sql)
    # print rows
    if len(rows) == 1:
        row = rows[0]
        org_id = row[0]
        return org_id
    return None

def write(msg, fOut):
    print msg
    fOut.write("%s\n"%(msg))

def getXmlCache(mssgdoc_id, fileName, debug = False):
    xml = ""
    if os.path.exists(fileName):
        if debug:
            print "File %s exists already, getting contents"%(fileName)
        xml = file(fileName).read()
    else:
        if debug:
            print "File %s does not exist.  Getting xml from mssgdoc_id=%s and caching it."%(fileName, mssgdoc_id)
        xml = getXml(mssgdoc_id)
        fOut = file(fileName, "w")
        fOut.write(xml)
        fOut.close()
    return xml

mapDbnamesToConnstrings = {}
setConnStrings(mapDbnamesToConnstrings)
## conns: Map of Connections -- name ==> connection
conns = setupConnections(mapDbnamesToConnstrings)

connNewtm = conns['newtradmarket']
connMS = conns['mssg']
conn = connNewtm

connNewtm2 = getConn(mapDbnamesToConnstrings["newtradmarket"])

sql = sqlCostplus

# rows = dbutils.getRows(connNewtm, sqlCostplus)
curs = conn.cursor()
curs.execute(sql)
rows = curs.fetchall()

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

cpOut = file("costplus_agent_fix.csv", "w")


## print Header
write( "ponum,om_po_id,intaudit_id,mssgdoc_id,code,org_id,filename", cpOut)

numAgents = 0

for r in rows:
    ponum = getColumn('ponum', r, colNames)
    om_po_id = getColumn('om_po_id', r, colNames)
    mssgdoc_id = getColumn('mssgdoc_id', r, colNames)
    intaudit_id = getColumn('intaudit_id', r, colNames)

    fName = r"CostPlusXml\POnum-%s_MssgDocId-%s.xml"%(ponum, mssgdoc_id)
    
    xml = getXmlCache(mssgdoc_id, fName, True)

    xmlTree = ET.fromstring(xml)

    for node1 in xmlTree:
        if node1.tag == "Order":
            for node2 in node1:
                if node2.tag == "Header":
                    for hdrnode in node2:
                        if hdrnode.tag == "PartyInfo":
                            party = hdrnode
                            if party.findtext("Type") == "Agent":
                                numAgents = numAgents + 1
                                agent = party
                                agentCode = party.findtext("Code")
                                
                                pt_org_id = getOrgForCode(agentCode, connNewtm2)
                                # print "PONum|%s|Agent|%s|Type|%s|Code|%s|pt_org_id|%s|filename|%s" %(ponum, party, party.findtext("Type"), agentCode, pt_org_id, fName)
                                write( "%s,%s,%s,%s,%s,%s,%s" %(ponum, om_po_id, intaudit_id, mssgdoc_id, agentCode, pt_org_id, fName), cpOut)

print "\n\nRows: %s, numAgents: %s"%(len(rows), numAgents)                                

cpOut.close()
