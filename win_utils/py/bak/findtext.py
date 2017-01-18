
pdocs = r"""
tags.append("Order/Header/OrderMessageID")
tags.append("Order/Header/OrderNumber")
tags.append("Order/Header/OrderDateTime")
tags.append("Order/Header/PaymentTerms")
tags.append("Order/Header/OrderPaymentMethod/")
tags.append("Order/Header/OrderPaymentTerms/PaymentTerms")
"""
## findtext(xmlText, xpaths)

import sys, os, urllib2, re
import xml.etree.ElementTree as ET # Python 2.5

class FindText:
    xmlText = ""
    xpaths = []
    errorStatus = 0   # 1 = failed to parse, 2=no text, 3=No xpaths
        
    def __init__(self, xmlText, xpaths, data={}):        
        self.xmlText = xmlText
        self.xpaths = xpaths
        self.data = data

        self.process()

    def process(self):
        ## parse xml
        ## print ("In FindText.process ...")
        try:
            xmlTree = ET.fromstring(self.xmlText)

            ## find xpaths
            for xpath in self.xpaths:
                # print ("%s"%(xpath))
                cell = ""
                try:
                    cell = xmlTree.findtext(xpath)
                except:
                    cell = "?"
                    # print "Failed"
                    
                ## print "%s ==> %s"%(xpath, cell)
                self.data[xpath] = cell

                # Now if xpath is "%CityCode", then get Qualifier attribute
                # self.data['Qual'] = 'Qual123'
                # self.data["xpath_"+xpath] = "||%s||"%(xpath)
            
                if str(xpath).endswith("CityCode"):
                    # self.data['Checking Qual'] = 'Qual 1232112'
                    cc = xmlTree.find(xpath)    # element
                    ccq = cc.attrib["Qualifier"]    # attr
                    self.data[xpath+"_Qualifier"] = ccq     

        except:
            errorStatus = 1        

    def getData(self):
        # (self.data.keys())
        return self.data

r"""
if len(sys.argv) < 5:
    sys.exit()

print "****************** in findtext ************ "

xmlFn = r"C:\GT\wsi\test\test_noCitCode.xml"
xpathsFn = r"C:\GT\wsi\asn_city_xpaths.txt"

argv = sys.argv
if len(argv) >= 2:
    xmlFn = argv[1]
if len(argv) >= 3:
    xpathsFn = argv[2]

## params read in, now do the test
xmltext = file(xmlFn).read()

xpaths = []
for line in file(xpathsFn).readlines():
    xpaths.append(line.strip())

data3 = {}
data3['filename'] = xmlFn

ft = FindText(xmltext, xpaths, data3)
data = ft.getData()

s1 = set(xpaths)
s2 = set(data.keys())
s3 = s2.difference(s1)
# print "%s\n- %s \n= %s "%(s1,s2,s3)
for x in s3:
  xpaths.append(x)

# print "xpaths=%s"%(xpaths)

print "\n%s is inputFile with %s bytes."%(xmlFn, len(xmltext))
print "%s is xpaths FileName with %s xpaths defined \n\n"%(xpathsFn, len(xpaths))

xpaths.sort()
for xp in xpaths:
    print ("%s: %s => %s "%(xmlFn, xp, data.get(xp, 'null')))
"""
