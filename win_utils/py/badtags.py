import os
import sys

class BadTags:

    def __init__(self, startDir):
        self.startDir = startDir
        self.process()

    def process(self):
        entries = 0
        
        for (path, dirs, files) in os.walk(self.startDir):
            ## Whole directory is on branch
            for f in files:
                # print f
                if f == "Tag" and path.find("CVS") >= 0:
                    msg = "Tag file found here: %s" %(path)
                    tagInfo = file("%s/%s"%(path, f)).read()
                    print "%s ==> %s " %(msg, tagInfo)

                if f == "Entries" and path.find("CVS") >= 0:
                    entries = entries + 1
                    fEntries = file("%s/%s"%(path, f))
                    for l in fEntries.readlines():
                        l = l.strip()
                        if l.find(r"//T") >=0 and l.find(r"//T:") < 0:
                            print r"%s/%s shows branched file: %s"%(path,f,l)

        print "Checked %s CVS/Entries files for signs of files not on Head or Main branch."%(entries)

#for a in sys.argv:
#    print a
    
b = BadTags(sys.argv[1])
