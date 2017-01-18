
fsrc = file("cpwmxml_ansi.rpt")
fdnp = file("cpwm_dnp.txt", "w")

uniq = {}

i = 0
for l in fsrc.readlines():
    i = i +1
    l = l.strip()
    lastund = l.rindex("_")
    if lastund > 0:
        l = l[0:lastund]
    l = l + "_DO_NOT_PROCESS"
    # print l
    uniq[l] = l
    # if i > 10
    #   break

fkeys = uniq.keys()
fkeys.sort()
for e in fkeys:
    fdnp.write(e + "\n")
    print e

print ("Created unique list of EDI files -- %i entries from %i xml files " %(len(fkeys), i))

fsrc.close()
fdnp.close()
