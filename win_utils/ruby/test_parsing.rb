# Test parsing ...

fn = "d:\\utils\\ruby\\xml\\po1.xml"
lines = File.readlines(fn)

def find_data_in_tag tag, lines
	found = []
	lines.each do |x|
		match = /<#{tag}>(.*)<\/#{tag}>/.match(x)
		found << match[1] if match && match.size > 1
	end
	found
end

print find_data_in_tag "OrderNumber", lines


def debugging

	lines = File.readlines(fn)

	# use x for line l because l and | look too similar=
	lines.each do |x|
		if x =~ /<OrderNumber>/
			puts x
			match = /<OrderNumber>(.*)<\/OrderNumber>/.match(x)
			puts match
			puts match.size
			0..match.size {|i| puts "match[#{i}] = #{match[i]} " }
			puts match[0]		# Regex => whole match is match[0]
			puts match[1]		# (.*) is actual OrderNumber we need
			# match.each {|m| puts "match array item: #{m} "}
		end	
	end
end
