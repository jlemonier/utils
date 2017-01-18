## walk through directories
## find every jar
## list every jar with each class

from os.path import join, getsize
import os, sys
import os, glob, time
import zipfile

def jarInfo(fnJar):
    z = zipfile.ZipFile(fnJar, "r")
    for filename in z.namelist():
        info = z.getinfo(filename)
        print "%s\t\t|%s\t\t|%s"%(fnJar, filename, info.date_time)

def findJar(dir):
    print "in findJar %s"%(dir)
    for root, dirs, files in os.walk(dir):
        # print root, "consumes",
        # print sum(getsize(join(root, name)) for name in files),
        # rpint "bytes in", len(files), "non-directory files"
        for f in files:
            lcf = f.lower()
            if lcf.endswith(".jar") or lcf.endswith(".zip"):
                fn = "%s\\%s"%(root, f)
                jarInfo(fn)

def findClass(dir):
    i = 1
    print "in findClass %s"%(dir)
    for root, dirs, files in os.walk(dir):
        for f in files:
            # i = i + 1
            lcf = f.lower()
            if lcf.endswith(".class"):
                fn = "%s\\%s"%(root, f)
                fmod = time.localtime(os.stat(fn)[8])
                fmod2 = time.strftime("%y/%m/%d %H:%M", fmod)
                print "%s\t\t|%s\t\t|%s"%(fn, fn, fmod2)

dirs = []
dirs.append(r"C:\src\Head\tradiant")
dirs.append(r"C:\apps\bea9\weblogic9")

# dirs = []
# dirs.append(r"C:\src\Head\tradiant\build")

for d in dirs:
    findClass(d)
    findJar(d)

# jarInfo(r"C:\src\Head\tradiant\release\lib\avalon-framework.jar")


    
"""
z = zipfile.ZipFile("zipfile.zip", "rb")
for filename in z.namelist():
        print filename
        bytes = z.read(filename)
        print len(bytes)

"""
