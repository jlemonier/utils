
# procs = %w{ C:\code\gtnexus\development\modules\main\tradiant\release\sql\rel\jitterbit\func }[0]
procs = %w{ C:\code\gtnexus\development\modules\main\tradiant\release\sql\rel\jitterbit\proc\orig }[0]

puts procs

Dir.entries(procs).select {|f| !File.directory? f}.each do |f|
	f = f.strip
	f2 = f.gsub("dbo.", "").gsub("\.StoredProcedure\.", ".").gsub("\.UserDefinedFunction\.", ".")
	
	puts "#{f} => #{f2} "
	
	if f.eql? f2
	  puts "#{f} does not have dbo.  -- skipping"
	  next
	end
	
	puts "#{f} => #{f2}"
	
	s1 = File.join(procs, f)
	s2 = File.join(procs, f2)
	File.rename(s1, s2)
	
end

Dir.entries(procs).select {|f| !File.directory? f}.each do |f|
	# Now remove: Use Jitterbit go
	lines = File.readlines(File.join(procs, f))
	
	# puts lines[0]
	# puts lines[1]
	
	if (lines[0] =~ /Use.*Jit/i && lines[1] =~ /go/i )
		puts "#{f} -- removing: #{lines[0]} #{lines[1]} now ..."
		File.open(File.join(procs,f), 'w') do |out|
			lines[2..-1].each { |line| out.print(line) }
		end
	else
		puts "#{f} does not have first 2 lines: Use Jitterbit / go - skipping changing"
	end
end

