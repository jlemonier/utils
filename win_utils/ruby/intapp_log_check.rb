
ifile = File.open("c:\\gt\\logs\\gtnexus-intapp.log.1")

patterns = {}
patterns["Party's Organization Key"] = 0
patterns["to 'com.tradiant.integration.orders.castor.MilestoneTime' due to the following error"] = 0
patterns["getCUCC"] = 0
patterns["Party's Organization Key"] = 0
patterns["Party's Organization Key"] = 0
patterns["Party's Organization Key"] = 0
patterns["Party's Organization Key"] = 0

lines = 0
alines = 0

while (line = ifile.gets)
	lines = lines + 1
	line =~ /^2010-11/ and alines = alines + 1
	puts line if lines < 5 or lines % 1000 == 0
	patterns.keys.each { |p|
		patterns[p] += 1 if line[p]
	}
	
	
	# break if lines > 5
		
end

print "Total lines: #{lines} - Log Statements: #{alines} \n\n"

patterns.keys.each { |k| print "#{patterns[k]} <= #{k}  \n" }
 


