import os
from os import path
import sys

## 0=object, 2=src-checksum, 4=dest-checksum
csvSqlObjectChanges = r"c:\gt\compare_qamain1_newtradmarket3.csv"

rootDir = r"c:\src\Head\tradiant\release\sql\rel"
displayRoot = r"\sql\rel"
args = len(sys.argv)

if args > 1:
    rootDir = args[1]

sep = os.sep

subdirs = []
subdirs.append("proc")
subdirs.append("view")
subdirs.append("func")

# tp_tfm_updatefinancerequest.sql => \sql\rel\tradefinance\proc\tp_tfm_updatefinancerequest.sql
mapFilesToDirs = {} # uses .sql

mapDirsToFiles = {} # uses .sql

def addItem(xmap, key, item):
    if xmap.has_key(key):
        xlist = xmap[key]
    else:
        xlist = []
        xmap[key] = xlist

    xlist.append(item)

def isSqlDirectory(path):
    for sdir in subdirs:
        if path.find("%s%s"%(sep,sdir)) >= 0:
            return True
    return False

# pass in: tp_daily_stats (or tp_daily_stats.sql) and get: /sql/rel/integration/proc/
def getDirForSqlCode(objectName):
    if mapFilesToDirs.has_key(objectName):
        result = mapFilesToDirs[objectName]
        print "File: %s is in directory: %s"%(objectName, result)
        return result
    return "?? Dir for: %s unknown "%(objectName)

def getFilesForDir(dirName):
    print dirName
    print mapDirsToFiles[dirName]
    if mapDirsToFiles.has_key(dirName):
        return mapDirsToFiles[dirName]
    return ""

iFileNum = 0

for (cpath, dirs, files) in os.walk(rootDir):
    # cpath ==> "c:\src\Head\tradiant\release\sql\rel\xx\file2.sql"
    # cpath2 ==> \sql\rel\xx\file2.sql ## defined by displayRoot above
    cpathOrig = cpath
    cpath = cpath[cpath.find(displayRoot):]
    # print "%s => %s"%(cpath2, cpath)
    
    # Skip CVS directories
    if path.split(cpath)[1] == "CVS":
        continue
    # Skip non-code directories
    # print "%s is code? => %s "%(cpath, isSqlDirectory(cpath))
    if not isSqlDirectory(cpath):
        continue
    
    for f in files:
        iFileNum = iFileNum + 1
        # Only .sql files
        if f.lower().endswith(".sql"):
            if iFileNum % 100 == 0 or iFileNum < 10:
                print os.path.join ("%s) %s%s%s"%(iFileNum, cpath, sep, f))
            mapFilesToDirs[f] = cpath
            addItem(mapDirsToFiles, cpath, f)


getDirForSqlCode("tp_daily_stats.sql")

testDir1 = r"\sql\rel\ex\func"
print getFilesForDir(testDir1)

for xdir, xfiles in mapDirsToFiles.items():
    if xdir == testDir1:
        print " testDir1: %s ==> %s"%(xdir, xfiles)
    # print "[[%s]]"%(xdir)
    # print "%s ==> %s"%(xdir, xfiles)


## 0=object, 2=src-checksum, 4=dest-checksum
csvSqlObjectChanges = r"c:\gt\compare_qamain1_newtradmarket3.csv"

mapObjectToChanged = {}
i = 0
for line in file(csvSqlObjectChanges).readlines():
    i = i + 1
    if i < 1:
        continue  # skip header row
    line = line.strip()
    rec = line.split(",")
    if len(rec) >= 5:
        sqlobject = rec[0]+".sql"   ## adding .sql to match our files and other maps
        changed = rec[2] != rec[4]
        mapObjectToChanged[sqlobject] = changed
    else:
        print "Cannot determine changes for line: %s"%(line)

## Now loop through directories
for xdir, xfiles in mapDirsToFiles.items():
    changedFiles = []
    for f in xfiles:
        if mapObjectToChanged.has_key(f):
            changed = mapObjectToChanged[f]
            if changed:
                changedFiles.append(f)
        else:
            print "%s not found in data for objects changed"%(f)
    print "%s => \n\tAll Files: %s \n\tChanged Files: %s "%(xdir, len(xfiles), len(changedFiles))
    print "%s => \n\tAll Files: %s \n\tChanged Files: %s "%(xdir, xfiles, changedFiles)
        
    
    
            
