import os
import sys
import re

fileNameInput = r"c:\gt\grid\wiki_page.txt"
if len(sys.argv) > 2:
    fileNameInput = sys.argv[1]
    
fileInput = file(fileNameInput)

fileOutput = file(fileNameInput+".grid.txt", "w")

# Define some patterns
patEndCarrot = re.compile("\^+$")   #  ** xyz ** ==> ^^ xyz ^^ ==> ^^ xyz
patWikiLink = re.compile("(\[\[).*?(\]\])")


for line in fileInput.readlines():
    line = line.strip()
    print line

    line2 = line.replace("*", "^")
    line2 = patEndCarrot.sub ('', line2)
    
    print line2

    wikiLink = patWikiLink.search(line2)
    if wikiLink:
        wl = wikiLink
        print wl
        print wl.group()
        print wl.span()

