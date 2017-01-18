require 'fileutils'


ids = File.open("vf.txt").read.split("\n")

if true

	ids.each do |id| 
		mfile = "#{id}.xml"
		# FileUtils.mv("#{id}.xml", "needed\\") if File.exists? mfile
		
		mfile = "needed\\#{id}.xml"
		# puts "#{mfile} missing" if not File.exists? mfile
		puts "#{id}" if not File.exists? mfile
		
	end

end

