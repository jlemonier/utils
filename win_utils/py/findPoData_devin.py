import sys, os, urllib2, re
import xml.etree.ElementTree as ET # Python 2.5

from findtext import FindText

fn = sys.argv[1]

class DataPrinter:
	l = {}
	def printData(self):
		print self.l
	def getData(self):
		return self.l
	def populateData(self):
		xmlTree = ET.parse(fn)

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
								printer.l[partyType] = poList
		

printer = DataPrinter()
printer.populateData()
printer.printData()