import re

bq = '(",)(?!")'
p = re.compile(bq)

def fixBadDq(s):
    return p.sub("``,", s)

s = r'''"001","HONG KONG","604-54733","NECKLACE,WHT,18",PEARL","2009-08-21T12:00:00.000","976855","7/28/09 6:18 PM","\purchase_order\xml\imp850p_127.edi_016000004.xml","858841483","7/28/09 6:18 PM","7887529","Hong Kong","1001502"'''
s2 = r'''"001","HONG KONG","604-54733","NECKLACE,WHT,18",PEARL","2009"'''

print fixBadDq(s)
print fixBadDq(s2)





