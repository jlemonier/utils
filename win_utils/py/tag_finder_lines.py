import sys, os, urllib2, re
import xml.etree.ElementTree as ET # Python 2.5
import findtext 

global linesPrinted
linesPrinted = 0

## Pass in <Tags> and get Map of Type=Value entries back
def getMapTags(tagsNode):
    tags = {}
    if tagsNode is not None:
        for tagNode in tagsNode:
            tagtype = tagNode.findtext("Type")  or ""
            tagval  = tagNode.findtext("Value") or ""
            tags[tagtype] = tagval
            # print "tags: %s "%(tags)
    return tags

def shortenColumnNames(col):
    col = col.replace("Order/Header/","")
    col = col.replace("TransactionInfo/","")
    return col

def writeHeader(fileObject, columnOrder):
    colsShorter = map(shortenColumnNames, columnOrder)
    lineOut = ",".join(colsShorter)
    writeIt(fileObject, lineOut, 0) ## 0 so it will print to display

def writeRecord(fileObject, dataMap, columnOrder=[], countPoFiles=2002):
    if len(columnOrder) == 0:
        columnOrder = dataMap.keys()
        columnOrder.sort()

    # csvFileOutPo.writerow(poTagRecord)    

    row = []
    for colName in columnOrder:
        # print "about to get colName: %s from keys: %s"%(colName, dataMap.keys())
        cellData = dataMap.get(colName) or ""   ## works always
        # cellData = dataMap[colName]   ## finds errors
        cellData.replace(","," ")
        cellData.replace("'","`")
        cellData.replace('"',"`")
        row.append(cellData)

    lineOut = ",".join(row)
    writeIt(fileObject, lineOut, countPoFiles)

def writeIt(fileObject, line, countPoFiles = 2002):

    if countPoFiles % 100 == 0 or countPoFiles < 10:
        print "PO File #%s ==> %s"%(countPoFiles, line)
    fileObject.write("%s\n"%(line))

    # fileObject.write("%s\n"%(",".join(map(shortenColumnNames, columnOrder))))
    # fileObject.write("%s\n"%(",".join(map(lambda x : dataMap.get(x), dataMap ))))

def writePoHeaderTags(fileOutPo, fullPath, rootXmlNode, countPoFiles):
    # fn = r"C:\GT\Liz\20091214_20091214_orders_po_xml_lizclaiborne\20091214\orders\po\xml\lizclaiborne\gtn850sup.o.827793.edi_156900001.xml"
    xmlText = file(fullPath).read()
    data = {}
    poData = findtext.FindText(xmlText, xpaths, data).data

    data["localfilename"] = fullPath
    
    headertags = rootXmlNode.find("Order/Header/Tags")

    # Has all PO Header level tags in a map.  But we must print 1-per-line
    poTagMap = getMapTags(headertags)

    # 1-record per  tag ... too many rows
    """
    for tagName in poTagMap.keys():
        poTagRecord = None
        poTagRecord = {}
        tagValue = poTagMap[tagName] or ""
        poTagRecord["TagName"] = tagName
        poTagRecord["TagValue"] = tagValue
        poTagRecord.update(poData)
    """
    poTagRecord = {}
    poTagRecord["TagData"] = map2str(poTagMap)
    poTagRecord.update(poData)
    writeRecord(fileOutPo, poTagRecord, poColumns, countPoFiles)

    return poTagRecord

## Pass poTagRecord so all/some columns at header level can be used on line level
def writePoLineTags(fileOutPoLine, fullPath, rootXmlNode, countPoFiles, poTagRecord):
    # PO Line Tags
    lineItemTags = []
    lineItemTags.append("LineItemNumber")
    lineItemTags.append("Quantity")
    lineItemTags.append("ProductCode")

    ponum = poTagRecord.get("Order/Header/OrderNumber")
    created = poTagRecord.get("TransactionInfo/Created")

    details = rootXmlNode.find("Order/Details")
    lineNum = 0
    if details is None:
        print "PO: %s File: %s had no lines. "%(ponum, poTagRecord.get("localfilename"))
        return
    for lineItem in details:
        lineNum = lineNum+1
        poLineTagRecord = {}
        for lineItemTag in lineItemTags:
            lineItemText = lineItem.findtext(lineItemTag)
            poLineTagRecord[lineItemTag] = lineItemText
        
        lineTags = lineItem.find("Tags")
        poLineTagMap = getMapTags(lineTags)
        poLineTagRecord["TagDataLine"] = map2str(poLineTagMap)
        poLineTagRecord["ponum"] = ponum
        poLineTagRecord["created"] = created
        poLineTagRecord["sender"] = poTagRecord.get("TransactionInfo/MessageSender")
        poLineTagRecord["receiver"] = poTagRecord.get("TransactionInfo/MessageRecipient")

        if countPoFiles % 100 == 0:
            print "line #%s => %s" %(lineNum, poLineTagRecord)

        writeRecord(fileOutPoLine, poLineTagRecord, poLineColumns, countPoFiles)

## How we need the map in SQL
def map2str(dataMap):
    s = str(dataMap)
    s = re.sub(r'[{}]', '', s)
    s = s.replace(",","|")
    s = s.replace("'","")
    return s
    
  
################################################################################
xpaths = {}
xpaths["Order/Header/OrderNumber"] = "ponum"
xpaths["Order/Header/OrderDateTime"] = "ordertime"
xpaths["Order/Header/Purpose"] = "purpose"
xpaths["Order/Header/CustomerCode"] = "custcode"
xpaths["Order/Header/CustomerDepartmentCode"] = "depcode"
# xpaths.append("Order/Header/CustomerDepartmentName")
xpaths["TransactionInfo/MessageSender"] = "sender"
xpaths["TransactionInfo/MessageRecipient"] = "recipient"
xpaths["TransactionInfo/Created"] = "created"
xpaths["TransactionInfo/FileName"] = "filename"

## Controls exact order and set of columns in .csv file
poColumns = []
poColumns.append("TagData")
poColumns = poColumns + xpaths.keys()   ## lose order here
poColumns.append("localfilename")

poLineColumns = []
poLineColumns.append("sender")
poLineColumns.append("receiver")
poLineColumns.append("ponum")
poLineColumns.append("created")                        
poLineColumns.append("LineItemNumber")
poLineColumns.append("ProductCode")
poLineColumns.append("TagDataLine")

fileOutSuffix = "csv"  # handy for tail
fileNameOutPo   = "poTags.%s"%(fileOutSuffix)
fileOutPo       = file(fileNameOutPo, "w")
fileOutPoLine   = file("poLineTags.%s"%(fileOutSuffix), "w")

################################################################################

# xmlText = """<?xml version="1.0" encoding="UTF-8"?><OrderMessage><TransactionInfo><MessageSender>LIZ</MessageSender><MessageRecipient>GTNEXUS</MessageRecipient><Created>2009-12-15T02:48:00</Created><FileName>gtn850sup.o.827793.edi</FileName></TransactionInfo><Order><Header><OrderNumber>0275500</OrderNumber><OrderDateTime>2009-12-15T12:00:00.000</OrderDateTime><Purpose>Update</Purpose><CustomerCode>LIZDIV</CustomerCode><CustomerDepartmentCode>JUICY COUTURE WMN FA-EUR</CustomerDepartmentCode><CustomerDepartmentName>JUICY COUTURE WMN FA-EUR</CustomerDepartmentName><OrderType>Cross-Border</OrderType><BuyerIdentification><IdentificationCode>J008</IdentificationCode><FirstName>J008</FirstName><LastName>J008</LastName></BuyerIdentification><PoReferenceNumber2>GBR</PoReferenceNumber2><PoReferenceNumber3>5510B</PoReferenceNumber3><PartyInfo><Type>ShipTo</Type><Code>PPE</Code><Name>PPE</Name><Address><AddressLine>PPE,GREAT SOUTH WEST ROAD</AddressLine><AddressLine>FELTHAM, MIDDLESEX,TW14 8NU,GBR</AddressLine></Address><City><CityName>FELTHAM, MIDDLESEX</CityName></City><PostalCode>TW14 8NU</PostalCode></PartyInfo><PartyInfo><Type>BillTo</Type><Code>J008</Code><Name>J008</Name><Address><AddressLine>J008,NO.8, FONGJIN ROAD THE WUXIAN,COUNTY ECONOMIC &amp; TECHNICAL</AddressLine><AddressLine>SUZHOU,CHN</AddressLine></Address><City><CityName>SUZHOU</CityName></City></PartyInfo><PartyInfo><Type>Supplier</Type><Code>J007</Code><Name>J007</Name><Address><AddressLine>J007,11TH FL., NO.376, SEC.4,JEN-AI RD.</AddressLine><AddressLine>TAIPEI,TWN</AddressLine></Address><City><CityName>TAIPEI</CityName></City></PartyInfo><Tags><Tag><Type>Factory Direct</Type><Value>No</Value></Tag><Tag><Type>Corporate Division</Type><Value>JUICY COUTURE WMN FA-EUR</Value></Tag><Tag><Type>Business Group</Type><Value>JUICY COUTURE</Value></Tag><Tag><Type>Legal Entity</Type><Value>JUICY COUTURE EUROPE LTD.</Value></Tag><Tag><Type>Direct Ship Indicator</Type></Tag></Tags></Header><Details><LineItem><LineItemNumber>473</LineItemNumber><Quantity Unit="Each">6</Quantity><FirstCostPrice>7.3</FirstCostPrice><ProductCode>YTRED372</ProductCode><ProductName>JACQUARD HEART TANK</ProductName><HarmonizedCode>473</HarmonizedCode><ManufacturerCode>YTE000059</ManufacturerCode><ProdReferenceNumber2>2, 609589073339, XS, ACCESSORY 2, 609589073346, S, ACCESSORY 1,  609589073353, M, ACCESSORY 1, 609589073360, L, ACCESSORY  </ProdReferenceNumber2><ProdReferenceNumber3>TBD</ProdReferenceNumber3><ProdReferenceNumber5>NA</ProdReferenceNumber5><ProdReferenceDate1>2009-11-03T12:00:00.000</ProdReferenceDate1><EventData><EventCode>CHN</EventCode><EventCodeDescription>CHN</EventCodeDescription></EventData><ETAFinalDestinationDate>2010-03-10T12:00:00.000</ETAFinalDestinationDate><ShipWindow><StartDate>2010-02-08T12:00:00.000</StartDate><EndDate>2010-02-08T12:00:00.000</EndDate></ShipWindow><TransportationMode>Ocean</TransportationMode><FinalDestination><LocationCode>PPE</LocationCode></FinalDestination><Tags><Tag><Type>Split</Type><Value>No</Value></Tag><Tag><Type>PO GOH/Cartons</Type><Value>Cartons</Value></Tag><Tag><Type>Product Type</Type><Value>Finished Goods</Value></Tag><Tag><Type>Property Mark</Type><Value>SJ776E</Value></Tag></Tags></LineItem></Details><Summary><NumberOfLineItems>1</NumberOfLineItems></Summary></Order></OrderMessage>"""
# fn = r"C:\GT\Liz\20091214_20091214_orders_po_xml_lizclaiborne\20091214\orders\po\xml\lizclaiborne\gtn850sup.o.827793.edi_156900001.xml"
# xmlText = file(fn).read()
# poData = FindText(xmlText, xpaths, data).data
# print "DEBUG 1 -- PO File Metadata: %s \n\n" %(poData)
# print "poColumns ==> %s "%(poColumns)
# headertags = root.find("Order/Header/Tags")
# Has all PO Header level tags in a map.  But we must print 1-per-line
# poTagMap = getMapTags(headertags)

######################
# PO Header Tags
######################

## Write 1st line of CSV file for PO data
writeHeader(fileOutPo, poColumns)

writeHeader(fileOutPoLine, poLineColumns)


startDir = r"C:\GT\Liz"     ## complete
## startDir = r"C:\GT\Liz\20091110_20091213_orders_po_xml_lizclaiborne\20091204\orders\po\xml\lizclaiborne"

## walk filesystem for xml files
##  - write PO Header Tag info (1 line per tag)
##  - write PO Line   Tag info (1 line per tag)
countPoFiles = 0
keepGoing = True

for fsroot, fsdirs, fsfiles in os.walk(startDir):
    for fileName in fsfiles:
        if fileName.lower().endswith(".xml") and keepGoing:
            countPoFiles = countPoFiles + 1
            if countPoFiles % 100 == 0:
                print "On PO File #%s => %s " %(countPoFiles, fileName)

            """
            if countPoFiles > 5:
                keepGoing = False
                break; """
            
            fullPath = r"%s\%s"%(fsroot, fileName)

            xmlTree = ET.parse(fullPath)
            rootXmlNode = xmlTree.getroot()

            ponum = writePoHeaderTags(fileOutPo, fullPath, rootXmlNode, countPoFiles)

            writePoLineTags(fileOutPoLine, fullPath, rootXmlNode, countPoFiles, ponum)

## Close the file
fileOutPo.close()
fileOutPoLine.close()

## Now turn it into a #tmp table
## sys.exec("csv2table %s"%(fileNameOutPo))
