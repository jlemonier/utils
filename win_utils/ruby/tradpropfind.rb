
ifile = File.open("C:\\GTSrc\\svn2\\trunk\\tradiant\\release\\properties\\tradiant.properties")

patterns = {}

lines = 0
alines = 0

while (line = ifile.gets)
	lines = lines + 1
	# puts line  if lines < 5 or lines % 1000 == 0
	
	showline = 0
	showline = 1 if line =~ /D:/
	showline = 1 if line =~ /localhost/
	showline = 1 if line =~ /t3:/
	showline = 1 if line =~ /\/tradiant\/release/
	
	showline = 0 if line =~ /^#/
	
	puts line if showline > 0
		
end

