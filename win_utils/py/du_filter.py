## du > file
##  10   ./.../y
##  200  ./.../x

## Keep only folders > 1mb
inputFile = file(r"c:\gt\jlemonier_cdrive_usage_totals.txt")
outputFile = file("%s.out"%(inputFile.name), "w")
line = inputFile.readline()

data = []

while line:
    line = line.strip()
    size,fdir = line.split('\t')
    size = int(size)

    if int(size) > 50000:
        msg = "%s,%s"%(size, fdir)
        data.append((size, fdir))
        # print (msg)
        # outputFile.write("%s\n"%(msg))

    line = inputFile.readline()

# data.reverse()
data.sort()
data.reverse()

for rec in data:
    msg = "%s,%s"%(rec[0], rec[1])
    print (msg)
    outputFile.write("%s\n"%(msg))
    

inputFile.close()
outputFile.close()
