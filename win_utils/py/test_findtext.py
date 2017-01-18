import sys, os, urllib2, re
import xml.etree.ElementTree as ET # Python 2.5

from findtext import FindText

data = {}
data['filename'] = 'xyz'


# fn = r"C:\GT\Liz\20091214_20091214_orders_po_xml_lizclaiborne\20091214\orders\po\xml\lizclaiborne\gtn850sup.o.827793.edi_156900001.xml"
# xmlText = """<?xml version="1.0" encoding="UTF-8"?><OrderMessage><TransactionInfo><MessageSender>LIZ</MessageSender><MessageRecipient>GTNEXUS</MessageRecipient><Created>2009-12-15T02:48:00</Created><FileName>gtn850sup.o.827793.edi</FileName></TransactionInfo><Order><Header><OrderNumber>0275500</OrderNumber><OrderDateTime>2009-12-15T12:00:00.000</OrderDateTime><Purpose>Update</Purpose><CustomerCode>LIZDIV</CustomerCode><CustomerDepartmentCode>JUICY COUTURE WMN FA-EUR</CustomerDepartmentCode><CustomerDepartmentName>JUICY COUTURE WMN FA-EUR</CustomerDepartmentName><OrderType>Cross-Border</OrderType><BuyerIdentification><IdentificationCode>J008</IdentificationCode><FirstName>J008</FirstName><LastName>J008</LastName></BuyerIdentification><PoReferenceNumber2>GBR</PoReferenceNumber2><PoReferenceNumber3>5510B</PoReferenceNumber3><PartyInfo><Type>ShipTo</Type><Code>PPE</Code><Name>PPE</Name><Address><AddressLine>PPE,GREAT SOUTH WEST ROAD</AddressLine><AddressLine>FELTHAM, MIDDLESEX,TW14 8NU,GBR</AddressLine></Address><City><CityName>FELTHAM, MIDDLESEX</CityName></City><PostalCode>TW14 8NU</PostalCode></PartyInfo><PartyInfo><Type>BillTo</Type><Code>J008</Code><Name>J008</Name><Address><AddressLine>J008,NO.8, FONGJIN ROAD THE WUXIAN,COUNTY ECONOMIC &amp; TECHNICAL</AddressLine><AddressLine>SUZHOU,CHN</AddressLine></Address><City><CityName>SUZHOU</CityName></City></PartyInfo><PartyInfo><Type>Supplier</Type><Code>J007</Code><Name>J007</Name><Address><AddressLine>J007,11TH FL., NO.376, SEC.4,JEN-AI RD.</AddressLine><AddressLine>TAIPEI,TWN</AddressLine></Address><City><CityName>TAIPEI</CityName></City></PartyInfo><Tags><Tag><Type>Factory Direct</Type><Value>No</Value></Tag><Tag><Type>Corporate Division</Type><Value>JUICY COUTURE WMN FA-EUR</Value></Tag><Tag><Type>Business Group</Type><Value>JUICY COUTURE</Value></Tag><Tag><Type>Legal Entity</Type><Value>JUICY COUTURE EUROPE LTD.</Value></Tag><Tag><Type>Direct Ship Indicator</Type></Tag></Tags></Header><Details><LineItem><LineItemNumber>473</LineItemNumber><Quantity Unit="Each">6</Quantity><FirstCostPrice>7.3</FirstCostPrice><ProductCode>YTRED372</ProductCode><ProductName>JACQUARD HEART TANK</ProductName><HarmonizedCode>473</HarmonizedCode><ManufacturerCode>YTE000059</ManufacturerCode><ProdReferenceNumber2>2, 609589073339, XS, ACCESSORY 2, 609589073346, S, ACCESSORY 1,  609589073353, M, ACCESSORY 1, 609589073360, L, ACCESSORY  </ProdReferenceNumber2><ProdReferenceNumber3>TBD</ProdReferenceNumber3><ProdReferenceNumber5>NA</ProdReferenceNumber5><ProdReferenceDate1>2009-11-03T12:00:00.000</ProdReferenceDate1><EventData><EventCode>CHN</EventCode><EventCodeDescription>CHN</EventCodeDescription></EventData><ETAFinalDestinationDate>2010-03-10T12:00:00.000</ETAFinalDestinationDate><ShipWindow><StartDate>2010-02-08T12:00:00.000</StartDate><EndDate>2010-02-08T12:00:00.000</EndDate></ShipWindow><TransportationMode>Ocean</TransportationMode><FinalDestination><LocationCode>PPE</LocationCode></FinalDestination><Tags><Tag><Type>Split</Type><Value>No</Value></Tag><Tag><Type>PO GOH/Cartons</Type><Value>Cartons</Value></Tag><Tag><Type>Product Type</Type><Value>Finished Goods</Value></Tag><Tag><Type>Property Mark</Type><Value>SJ776E</Value></Tag></Tags></LineItem></Details><Summary><NumberOfLineItems>1</NumberOfLineItems></Summary></Order></OrderMessage>"""

fn = r"J:\py\data\liz_file1.xml"
xmlText = file(fn).read()

xpaths = []
xpaths.append("TransactionInfo/MessageSender")
xpaths.append("TransactionInfo/MessageRecipient")  

ft = FindText(xmlText, xpaths, data)

print ft.data

# xmlTree = ET.fromstring(xmlText)

def sub(parent, tag):
    return ET.SubElement(parent, tag)


xmlTree = ET.parse(fn)


root = xmlTree.getroot()
for node1 in root:
    print "%s -- %s" %(node1.tag, node1)

    for node2 in node1:
        print "  %s -- %s" %(node2.tag, node2)

        if node2.tag == "Header":
            for hdrnodes in node2:
                if hdrnodes.tag == "Tags":
                  hdrTags = hdrnodes
                  print hdrTags
                  for tag in hdrTags:
                      print tag

print "findall now ... "
for node in root.findall('Tags'):
    print node,

# print order.find("Header")
# print "under Order"
# print order

for e in xmlTree.findall("Order/Tags"):
    print e

print root
print root.find("Order")
print root.find("Order")

headertags = root.find("Order").find("Header").find("Tags")
for n in headertags:
    tagtype = n.findtext("Type")
    tagval  = n.findtext("Value") or ""
    print " %s -> '%s' = '%s' "%(n.tag, tagtype, tagval)





