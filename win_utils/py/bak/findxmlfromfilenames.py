## Expects:
##  param1=inputfile
##  param2=xpath elements needed listed 1-per-row

## Produces:
##  1-line per-line of input
##  with extra columns represented by each xpath in 2nd param

import sys, os, re
from findtext import FindText

class FindTextInXmlFromFilenames:
    #  startDir = ""
    # xpaths = []
    # sep = "|"
    # fileExt = ".xml"
    # headerWritten = 0
    debugPri = 0
    errors = 0
    maxErrors = 10000000

    ## csvInput example
    ## om_po_id,pol_orig_city_id,pol_city_name,max_createtime,intaudit_id,filename,createtime
    ## 7349867,1002812,Manila,8/11/09 12:18 AM,865761479,\purchase_order\xml\imp860p_256_016005812.xml,8/11/09 12:18 AM
    ## 7469909,23960,Ningbo,8/12/09 12:15 AM,866452469,\purchase_order\xml\imp860p_318_016000073.xml,8/12/09 12:15 AM
    def __init__(self, csvInput, xpaths, outfile, sep=","):
        self.startDir = startDir
        self.xpaths   = xpaths
        self.outFile  = outfile
        self.sep      = sep
        
        self.headerWritten = 0
        self.counter = 0
        
        self.process()

    ## 1) Loop through csv input
    ## 2) For each file, find the xml, save it
    ## 3) use findtext to get desired elements
    ## 4) write this line w/ new columns to csv
    
    def process(self):

        # CityCode ==> CityCode_Qualifier added in findtext.py
        headers = self.xpaths
        headers2 = []
        for h in headers:
            print "header [%s]"%(h)
            headers2.append(h)
            if h.endswith("CityCode"):
                headers2.append(h+"_Qualifier")
        headers2.append("filename")
        headers2.append("filepath")
        headers = headers2
        
        # for root, dirs, files in os.walk(self.startDir):
        for root, dirs, files in os.walk(self.startDir):
            for fn in files:
                if self.errors > self.maxErrors:
                    print "returning to stop because maxErrors reached"
                    return
                if fn.endswith(self.fileExt):
                    inputFile = "%s/%s"%(root, fn)
                    inputText = file(inputFile).read()
                    self.debug("inputFile=%s Bytes=%s "%(inputFile, len(inputText)))
                    
                    data = {}
                    data["filename"] = fn
                    data["filepath"] = r"%s\%s"%(root,fn)
                    ft = FindText(inputText, self.xpaths, data)

                    data = ft.getData()
                    if len(data) > 2:
                        self.writeInfo(data, headers)
    
    def writeInfo(self, data, headers):
        try:
            ## print "data=%s"%(data)
        
            ## Header Once
            if self.headerWritten == 0:
                # self.write ("%s"%(self.sep.join(data.keys())))
                self.write ("%s"%(self.sep.join(headers)))
                self.headerWritten = 1
        
            ## Data row
            values = []
            for h in headers:
                v = data.get(h, '')
                # if v is None or len(v) == 0:
                #     v = ''
                values.append('"%s"'%(v))
            self.write ("%s"%(self.sep.join(values)))
        except:
            print "Failed in writeInfo: %s for data=%s"%(" || ".join(map(str, sys.exc_info())), data)
            self.write ("-- Failed record! %s"%(data))
            self.errors = self.errors +1

    def write(self, txt):
        self.outFile.write("%s\n"%(txt))
        print ("%s"%txt)
        

    def debug(self, msg):
        if self.debugPri > 0:
            print (msg)
        
