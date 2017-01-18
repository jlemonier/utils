
import os, sys

prefix = sys.argv[1] or ""
if len(prefix) < 1:
    print "Usage: prefix 53420-X-ALL-UP- to add this prefix to all files in the directory" 

i = 0
for fname in os.listdir("."):
    i = i + 1
    prefixi = prefix.replace("-X-", "-%s-"%(i))
    fname2 = prefixi + fname

    if fname.startswith(prefixi):
        print "%-60s => %s" %("SKIP Rename %s"%(fname), fname2)
    else:
        os.rename(fname, fname2)
        print "%-60s => %s" %("Rename %s"%(fname), fname2)
    
