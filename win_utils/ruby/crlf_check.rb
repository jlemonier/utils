# Find weird character in *.list ??

# C:\gtsrc\workspaces\march_2014_checkout\tradiant_agile_14_4_scrubbed\
# C:\gtsrc\workspaces\march_2014_checkout\tradiant_agile_14_4_scrubbed\modules\BusinessRuleFramework\buildfiles\gwtmodule.list

files = []
files << %w{C:\gtsrc\workspaces\march_2014_checkout\tradiant_agile_14_4_scrubbed\modules\BusinessRuleFramework\buildfiles\gwtmodule.list}[0]
files << %w{                                        c:\src\git_ctc\trad\tradiant\modules\BusinessRuleFramework\buildfiles\gwtmodule.list}[0]

files.each do |fn|
	puts "\n\nStarting: #{fn} ... \n"
	File.open(fn) do |f|
		# f.each_byte {|ch| print "#{ch.chr}=#{ch} - " }
		b = -1
		f.each_byte {|ch| b += 1; print "#{b}) #{ch} \n"; break if b > 30 }
	end
end