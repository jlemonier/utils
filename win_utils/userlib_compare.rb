# Find missing jars based on user library files

def standardize_jar_names (jar_list)
	# print "std: #{jar_list} \n"
	new_list = []
	jar_list.each do |j|
		next if j == nil # or if j.to_s.size <= 1
		# print "		j: #{j} - #{j.class} BEFORE \n"
		tokens = ["\/release\/lib\/", "\/test\/lib\/", "\/server\/lib\/", "\/bea10\/modules\/"]
		tokens.each {|token| j = j[j.index(token)..-1] if j.index(token) }
		# print "		j: #{j} - #{j.class} AFTER \n"
		new_list << j
	end
	new_list
end

# Find ALL jars in a filename
def list_jars(filename) 
	lines = File.readlines(filename)
	print ("file: #{filename} has #{lines.size} lines \n")
	
	jars = Hash.new(0)	# Default counter to 0
	lines.each do |n|
		# jars / scan in case more than 1 per line
		njars = n.scan(/path=\"(.*)\"/).flatten
		njars = standardize_jar_names(njars)
		njars.each {|j| jars[j] += 1 }
	end
	print ("file: #{filename} has jars listed X times: \n")
	jars.each {|j,ctr| print "	#{ctr} times - #{j}  \n " }
end

# List of files in startDir ending with *.userlibraries
in_files = Dir['s:/*.userlib*']

mapFnJars = {}

in_files.each do |f|
	print "#{f} \n"
	mapFnJars[f] = list_jars(f)
end

lists = mapFnJars.values

j1 = lists[0].keys
j2 = lists[1].keys

NL = "\t\n"

print ("Input Files: \n#{in_files.join(NL)} ")

print ("\n\n 2nd - 1st: \n #{(j2-j1).join(NL)}  " )
print ("\n\n 1st - 2nd: \n #{(j1-j2).join(NL)} " )


