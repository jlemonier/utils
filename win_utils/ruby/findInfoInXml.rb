
# xfiles = Dir.glob('\\\\pft2a\\ftpdrop$\\outboundbackupsentry\\20101109\\dhl_3pl\\out\\orders\\asn\\to_staples\\*.xml')
# xfiles = Dir.new("c:\\gt\\").glob("*.txt")
# xfiles = Dir.glob("c:\\gt", "*.txt")

require 'rexml/document'
include REXML

def get_file_as_string(filename)
  data = ''
  f = File.open(filename, "r") 
  f.each_line do |line|
    data += line
  end
  return data
end

def getText(doc, xpath)
	doc.elements.each(xpath) { |t|
		return t.text
	}
end

def getPartyInfo(doc, xpathParties, partyTypeNeeded, elements = ["Code","Name"])
	doc.elements.each(xpathParties) { |partyNode|
		partyType = getText(partyNode, "Type")
		# print "\n\n===>> #{partyNode} \n => #{partyType} \n\n"
		
		if partyType == partyTypeNeeded
			rc = []
			rc << "ShipmentFinalDest"
			elements.each { |e|
				etext = '"'+getText(partyNode, e) + '"'
				# print "======>> #{partyNode} \n => #{partyType} \n\n"
				rc << etext
			}
			return rc
		end
	}
	
	rc = []
	rc << "ShipmentFinalDest" << elements.map { |x| "No #{x} "}
	return rc
end


def getAsnData(data, filename)
	xmldoc = Document.new(data)
	root = xmldoc.root

	rc = []
	rc << getText(xmldoc,"ASNMessage/ASN/ShipmentID") 
	rc << getPartyInfo(xmldoc,"ASNMessage/ASN/PartyInfo", "ShipmentFinalDest") 
	rc << filename
	return rc.join(",")
end

dirs = []
# staplesDirs << "s:\\outboundbackupsentry\\20101109\\dhl_3pl\\out\\orders\\asn\\to_staples"
# staplesDirs << "s:\\outboundbackupsentry\\20101108\\dhl_3pl\\out\\orders\\asn\\to_staples"
# staplesDirs << "s:\\outboundbackupsentry\\20101107\\dhl_3pl\\out\\orders\\asn\\to_staples"

# dirs << "C:\\gt\\bugs\\staples\\63721\\asnsXXXX"
# dirs << "C:\\GT\\bugs\\Staples\\63721\\asns"

suffix = "\\dhl_3pl\\out\\orders\\asn\\to_staples"
backupRoot = "B:\\tn\\ftpdrop\\outboundbackupsentry" 
recentRoot = "S:\\outboundbackupsentry"


## Backup directories back to Oct 10th
for month in [11]
	for day in "01".."11"	# 31
		# dirs << backupRoot+"\\2010"+month.to_s+day.to_s+suffix
		dirs << recentRoot+"\\2010"+month.to_s+day.to_s+suffix
	end
end


dirs.each { |staplesDir|
	# print "---- checking #{staplesDir} \n"
	if not File.directory? staplesDir
		# print "#{staplesDir} does not exist ********* \n"
		next
	end
	
	day = "?"
	if staplesDir =~ /outboundbackupsentry\\(\d+)\\/
		day = $1	
	end
	
	
	
	
	Dir.new(staplesDir).each {|x| 
		fname = "#{staplesDir}\\#{x}"

		if fname["xml"] and not fname["DO_NOT"]
			data = get_file_as_string(fname)
			# data2 = data[0,20]
			data2 = getAsnData(data, fname)

			print "#{day},#{data2},\n"
		end
	}
}


