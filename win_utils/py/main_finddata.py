import os
import sys
from finddata import FindData

if len(sys.argv) >= 3:
    srcDir    = sys.argv[1]
    xpathsFn  = sys.argv[2]
    outFile   = sys.argv[3]
else:
    srcDir   = r"C:\GT\wsi\test"
    xpathsFn = r"C:\GT\wsi\asn_city_xpaths.txt"
    outFile  = r"C:\GT\wsi\test\output.csv"

print ("srcDir=%s \nxpaths=%s \noutFile=%s"%(srcDir, xpathsFn, outFile))

f = FindData(srcDir, xpathsFn, outFile)


