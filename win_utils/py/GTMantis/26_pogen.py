import os

pos = []
po2sys = {}
po2id  = {}

fin = file("26_posystem.txt")
for line in fin:
    line = line.strip()
    po,posys = line.split("|")
    po2sys[po] = posys
    pos.append("'%s'"%(po))

fin = file("26_po2id.txt")
for line in fin:
    line = line.strip()
    po,id = line.split("|")
    po2id[po] = id

for po in po2sys.keys():
    print "\n-- po=%s, om_po_id=%s, posystem=%s"%(po, po2id[po], po2sys[po])

    #      exec tp_save_tag 'HQPWBIMP', 'POSystem', 60001, 7815524, 35540
    print "exec tp_save_tag '%s', 'POSystem', 60001, %s, 35540 " %(po2sys[po], po2id[po])

print " ponum in (%s) " %(", ".join(pos))


    
    # print "exec tp_save_tag '%s', 'POSystem', 60001, 7815524, 35540 "
