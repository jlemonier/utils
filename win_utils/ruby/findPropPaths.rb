require "find"
# Walk all *.properties files and create *.properties.paths files with files that have / or \\

startDir = "c:/code/gtnexus/properties/gtnx"
Find.find(startDir) { |f|
	if f.end_with? ".properties"
		print "#{f} \n"
		
		File.open("#{f}.paths", 'w') { |out| 
			File.foreach(f).with_index do |line, line_num|
				if line =~ /\\\\\\\\/   # /\/|\\/
					puts "#{line_num}: #{line}" 
					out.write ("#{line_num}: #{line}")\
				end
			end
		}
			
	end

}

