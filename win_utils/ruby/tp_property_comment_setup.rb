# C:/apps1/ws1/tradiant_agile_13_4/release/properties_backup_2013_1/bean.properties

startDir = "C:/apps1/ws1/tradiant_agile_13_4/release/properties_backup_2013_1/"

def process_file filename, startDir
	cc = []		# current_comment
	
	infile = File.new(File.join(startDir, filename))
	lines = infile.readlines
	lines.each do |n|
		n = n.strip
		n = n.gsub("'", "''")	# Replace ' with '' (two tics) for SQL to work correctly
		case 
			when n =~ /^#/		# Add this comment line to current comment
				cc.push n
			when n =~ /^\s*$/	# found blank line ... clear comment (consider not doing this?  Some comments are not related to a key=value
				cc = []
			when n =~ /^\w+=\w+/	# found key=value
				if cc.size > 0
					key,value = n.split('=', 2)
					print "exec tp_property_comment '#{filename}', '#{key.strip}', '#{cc.join "\\n"}'  \n"
				end
				cc = []		# clear comment regardless of whether a comment existed for that key
		end
	end
end

Dir.entries(startDir).each do |pf|
	next if File.directory? pf
	
	print "\n\n-- Found file: #{pf} \n"
	
	process_file pf, startDir
	
end