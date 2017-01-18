pdocs = r"""
Example Batch File:
title 1. running wsi check 4 partners for 90 days 2. creating sql from csv
python c:\apps\utils\py\main_finddata.py c:\gt\wsi\xml c:\gt\wsi\asn_city_xpaths.txt c:\gt\wsi\output4p.csv > output4.log 2> output4.err
csv2table output4p.csv
1) class FindData (in finddata.py)
2) FindData.process uses class findXmlInFiles (in findxmlinfiles.py)
3) findXmlInFiles.process walks through directories
and uses class FindText (in findtext.py)
to find specific xpath text & attributes inside of xml
"""

from findxmlinfiles import findXmlInFiles

class FindData:
    srcDir =""
    def __init__(self, src, xpathsfn, outfilefn):
        ## print ("In FindData __init__")
        self.srcDir = src
        self.xpathsFn = xpathsfn
        self.outfileFn = outfilefn
        
        self.outfile = file(self.outfileFn, "w")

        self.xpaths = []
        for line in file(self.xpathsFn).readlines():
            self.xpaths.append(line.strip())

        print ("\n\n Finding Data in xml starting in directory: %s \n"%(src))
        print ("\n   Writing Data to: %s"%(outfilefn))
        print ("\n   Finding xpaths: %s \n\n"%(", ".join(self.xpaths)))
        self.process()

    def process(self):
        finder = findXmlInFiles(self.srcDir, self.xpaths, self.outfile)

