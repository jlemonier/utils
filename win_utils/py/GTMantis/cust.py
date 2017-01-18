## simple python script to take a list of customers and generate a MySQL enum for bugs.customer column definition.

# as of: June 4th 6pm
# -- ENUM('-','ALL CUSTOMERS','American Eagle','American Standard','APL','BMS','Cargill','CAT Logistics','CEVA','CEVA-Microsoft','Charming Shoppes','China Shipping','CNH','Cost Plus','CP Ships','Crowley','CSAV','CSO','DHL','DuPont','Engineering','Furniture Brands','GAP','GBE','Grainger','GTN','Hanjin','Hapag-Llyod','Home Depot','HP','Hyundai','Imperial Tobacco','KB Toys','K-Line','Kmart','Kraft Foods','Liz Claiborne','Maersk Logistics','MOL','Nestle','OSA','PBD','P&G','Polo Ralph Lauren','PVH','Product Manager','Rhodia','Seagha','Sears Canada','SCA','Schenker','SPARK','UPS','Vis2005','Wal-Mart','Warnaco','Westwood','Weyerhaeuser','WSI','Xerox','Yang Ming','Yazaki','ZF','Zim')


import os, sys

# enum = ['-','ALL CUSTOMERS','American Eagle','American Standard','APL','BMS','Cargill','CAT Logistics','CEVA','CEVA-Microsoft','Charming Shoppes','China Shipping','CNH','Cost Plus','CP Ships','Crowley','CSAV','CSO','DHL','DuPont','Engineering','Furniture Brands','GAP','GBE','Grainger','GTN','Hanjin','Hapag-Llyod','Home Depot','HP','Hyundai','Imperial Tobacco','KB Toys','K-Line','Kmart','Kraft Foods','Liz Claiborne','Maersk Logistics','MOL','Nestle','OSA','PBD','P&G','Polo Ralph Lauren','PVH','Product Manager','Rhodia','Seagha','Sears Canada','SCA','Schenker','SPARK','UPS','Vis2005','Wal-Mart','Warnaco','Westwood','Weyerhaeuser','WSI','Xerox','Yang Ming','Yazaki','ZF','Zim']
#for c in enum:
#     print c

customers = """-
ALL CUSTOMERS
Adisseo
American Eagle
American Standard
APL
BMS
BritishAmericanTobacco
Cardinal Health
Cargill
CAT Logistics
Celanese
CEVA
CEVA-Microsoft
Charming Shoppes
China Shipping
CNH
Connell Bros.
Corning Inc.
Cost Plus
CP Ships
Crowley
CSAV
CSO
Daimler
Dachser
Del Monte Foods Company
DHL
Dicks Sporting Goods
DuPont
Eagle Global Logistics LP
Engineering
Furniture Brands
GAP
GBE
Grainger
GTN
Hanjin
Hapag-Llyod
Hellmann
Hewlett Packard Company
Home Depot
HP
Hyundai
Imperial Tobacco
Inditex
INVISTA
International Paper
JFHillebrand
Johnson & Johnson
KB Toys
K-Line
Kmart
Kraft Foods
KuehneNagel
Liz Claiborne
Maersk Logistics
MalloryAlexander
Mattel
MOL
Nestle
Nike, Inc.
NYK
OSA
Otto International
Panalpina
PBD
P&G
Philips
Philips Van Heusen Corp.
Polo Ralph Lauren
Procter & Gamble Company
PVH
Product Manager
Restoration Hardware
Rhodia
SA Recycling
Seagha
Sears Canada
Sears Holdings
SCA
Schenker
SM21
SPARK
Suzano Papel e Celulose
Transalpe
Votorantim
Unipac
UPS
Vis2005
Wal-Mart
Warnaco
Westwood
Weyerhaeuser
WSI
Wyeth
Xerox
Yang Ming
Yazaki
ZF
Zim"""

custlist = customers.split("\n")
custlist.sort()

for c in custlist:
    print c

enum = "ENUM("
for c in custlist:
    c2 = "'%s', "%(c)
    enum = enum + c2
enum = enum + ")"

print enum
    
