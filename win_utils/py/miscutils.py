import os
import sys
import pickle

## md5 is built-in to Python 2.6
from md5 import md5

def checkSum(str):
    if str is not None:
        return md5(str).hexdigest()
    return None

## unpickle / load
def unpickle2(fileName, defaultObj):
    try:
        myObj = pickle.load(file(fileName))
        return myObj
    except:
        print [x for x in sys.exc_info()]
        return defaultObj

def pickle2(obj, fileName, debug = False):
    try:
        if debug:
            print "** Pickling \n\t%s \nt\tto %s "%(obj, fileName)
        fileObj = file(fileName, "w")
        pickle.dump(obj, fileObj)
        fileObj.close()

        if debug:
            print "\n\t * Done Pickling "
    except:
        print [x for x in sys.exc_info()]
