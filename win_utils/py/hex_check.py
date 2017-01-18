# -*- coding: cp1252 -*-

"""
select * from tt_vessel where name = 'OOCL ANTWERP' and org_id = 2112 -- NOT a space.  It has value 160 instead of 32
select * from tt_vessel where name = 'OOCL ANTWERP' and org_id = 2112
select * from tt_vessel where name like 'OOCL ANT%' and org_id = 2112

OOCL ANTWERP - bad
 O => 79
 O => 79
 C => 67
 L => 76
   => 160
 A => 65
 N => 78
 T => 84
 W => 87
 E => 69
 R => 82
 P => 80
   => 32
 - => 45
   => 32
 b => 98
 a => 97
 d => 100
OOCL ANTWERP - good
 O => 79
 O => 79
 C => 67
 L => 76
   => 32
 A => 65
 N => 78
 T => 84
 W => 87
 E => 69
 R => 82
 P => 80
   => 32
 - => 45
   => 32
 g => 103
 o => 111
 o => 111
 d => 100
>>> 
"""

inputString = "ab cd"

inputs = []
inputs.append('OOCL ANTWERP - bad') # Space is 160 instead of 32
inputs.append('OOCL ANTWERP - good') # Space is  32 as expected
# inputs.append(inputString)

for testString in inputs:
    print "%s" %(testString)
    for c in testString:
        print " %s => %s" %(c, ord(c))
