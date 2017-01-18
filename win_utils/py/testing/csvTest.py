
import os
import csv

data = {}
data['a'] = '1A'
data['b'] = '2B'
data['c'] = '3C'

data['Order/Header/D'] = '4DDD'

cols = data.keys()
for c in cols:
    print c

cols2 = []
for k in data.keys():
    cols2.append(k)
    
print cols2.get(1)

outFileName = "testOut.csv"
csvFile = file(outFileName, "w")
csvWriter = csv.DictWriter(csvFile, cols)

csvWriter.writerow(data.keys())
csvWriter.writerow(data)

csvFile.close()

