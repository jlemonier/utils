import sys
import urllib2
import os

baseUrl = "http://pnetapp3a:7101/sysmgmt/mssggrab_sitescope.jsp?mssgdocid="

def getMssgDocData(mssgDocId):
    try:
        mssgDataUrl = "%s%s"%(baseUrl, mssgDocId)
        pipe = urllib2.urlopen(mssgDataUrl)
        data = pipe.read()
        pipe.close()

        return data
    except:
        return None

# newCopy=True will not get the file again
def getMssgDocWriteData(mssgDocId, fileName=None, outputDir=r"c:\gt\data\mssgserver", newCopy=False):
    try:
        
        if fileName is None:
            fileName = "%s.xml"%(mssgDocId)
        filePath = r"%s\%s"%(outputDir, fileName)

        fexists = os.path.exists(filePath)

        if fexists and not newCopy:
            print ("%s ALREADY EXISTS - NOT COPYING AGAIN - newCopy=%s "%(filePath, newCopy))
            return

        else:
            if fexists:
                print ("%s ALREADY EXISTS - GETTING AGAIN - newCopy=%s"%(filePath, newCopy))
        
            data = getMssgDocData(mssgDocId)
            fOut = file(filePath, "w")
            fOut.write(data)
            print ("Wrote %s via MssgServer with %s bytes"%(filePath, len(data)))
            fOut.close()
    except:
        print (sys.exc_info())
    
