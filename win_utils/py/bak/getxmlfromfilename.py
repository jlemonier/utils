import traceback
import sys, os, urllib2, re


## 
class GetXmlFromFileName:
    
    def __init__(self, filename, MessageType='orders', debug=0):
        
        self.fileName = filename
        self.baseName = os.path.basename(self.fileName)
        self.url_search = "http://pfile1a/file_search_results.asp?EnvironmentType=prod&MessageType=%s&FileNameValue=%s" %(MessageType, self.baseName)
        self.dataUrl = "??"
        self.data = ""
        
        self.status = "ok"
        try:
          self.process()
        except:
          self.status = "Failed"
          self.printEx(sys.exc_info())

    def getData(self, url):
        try:
            pipe = urllib2.urlopen(url)
            xdata = pipe.read()
            return xdata
        except:
            # writeErr("no data from url=%s "%(url))
            self.printEx(sys.exc_info())
            return None

    def mydata(self):
        if self.data is None:
            return "???"
        else:
            return self.data

    def printEx(self, ex):
        for x in ex:
            print str(x)
        tb = ex[2]
        traceback.print_tb(tb)
        
    def myurl(self):
        return self.dataUrl

    def info(self):
        print "1) filename   => %s"%(self.fileName)
        print "2) basename   => %s"%(self.baseName)
        print "3) url_search => %s"%(self.url_search)
        print "4) dataUrl    => %s"%(self.dataUrl)
        print "5) bytes      => %s"%(len(self.data))
        print "6) status     => %s"%(self.status)
        print "7) Data       =>\n>>>>\n%s\n<<<< -- End Data"%(xget.mydata())

    def process(self):

        ## info is "links to the data"
        info = self.getData(self.url_search)
        headEndIndex = info.find("</HEAD>")+7
        # print "info before: %s"%info # good
        if headEndIndex <= 0:
            headEndIndex = 0
        info = info[headEndIndex:]
        info = re.sub("[\r\n]", "", info)

        info2 = info.split("|")
        if len(info2) >= 4:
            self.dataUrl = info2[3]
            self.data = self.getData(self.dataUrl)
        

argv = sys.argv
files = []
if len(argv) >= 2:
    files.append(argv[1])
#else:
    # filename = r"\purchase_order\xml\imp860p_256_016005812.xml"
    
    # files.append(r"\purchase_order\xml\imp860p_256_016005812.xml")
    # files.append(r"\purchase_order\xml\imp860p_318_016000074.xml")
    
if len(files) > 0:
    for fn in files:
        xget = GetXmlFromFileName(filename=fn,debug=1)
        xget.info()
    
