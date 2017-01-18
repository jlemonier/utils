import sys, os, urllib2, re
import xml.etree.ElementTree as ET # Python 2.5

from findtext import FindText

# fn = sys.argv[1]

class DataPrinter:

    def __init__(self, xmlFileName):
            self.partyTypes = {}
            self.xmlFileName = xmlFileName
            # print "file name: %s"%(self.xmlFileName)
            # print "file data: %s"%("\n".join(file(self.xmlFileName).readlines()))
            self.trimXml()
            self.populateData()

    def trimXml(self):
        data = file(self.xmlFileName).read().strip()
        fout = file(self.xmlFileName, "w")
        fout.write(data)
        fout.close()
                
    def printData(self):
        # print "In printData - %s"%(self.l)
        for ptype in self.partyTypes:
            print "%s => %s"%(ptype, self.partyTypes[ptype])
    def getData(self):
        return self.partyTypes
    def getData2(self):
        return self.getData()
    def populateData(self):
        xmlTree = ET.parse(self.xmlFileName)

        root = xmlTree.getroot()
        for node1 in root:
            if node1.tag == "TransactionInfo":
                fileName = node1.findtext("FileName")
            elif node1.tag == "Order":
                for node2 in node1:
                    if node2.tag == "Header":
                        ponum = node2.findtext("OrderNumber")
                        for hdrnodes in node2:
                        
                            if hdrnodes.tag == "PartyInfo":
                                poList = []
                                
                                hdrTags = hdrnodes
                                partyType = hdrTags.findtext("Type")
                                partyCode = hdrTags.findtext("Code")
                                partyName = hdrTags.findtext("Name")
                                
                                poList.append(fileName)
                                poList.append(ponum)
                                #poList.append(partyType)
                                poList.append(partyCode)
                                poList.append(partyName)
                                
                                for tag in hdrTags:
                                    if tag.tag == "City":
                                        cityCode = tag.findtext("CityCode")
                                        for subTag in tag:
                                            if subTag.tag == "CityCode":
                                                qualifier = subTag.get("Qualifier")
                                                poList.append(cityCode)
                                                poList.append(qualifier)
                                # printer.l[partyType] = poList
                                # print poList
                                self.partyTypes[partyType] = poList
        

# printer = DataPrinter()
# printer.populateData()
# printer.printData()

def testFile(fn):
    test1 = DataPrinter(fn)
    test1.printData()

root = r"c:\gt\bugs\VF"
f1 = root+r"\xml\28376755.xml"
f2 = root+r"\xml\28376758.xml"
testFile(f2)
