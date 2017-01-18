
# Split CSV into #tmp

# finput = %w{ D:\GoogleDrive\GTNexus\JitterBit\DataFix_March13_2015\PO_SO_3_cols.csv }[0]
finput = ARGV[0] || %w{ D:\GoogleDrive\GTNexus\JitterBit\DataFix_March13_2015\ASN_3_cols.csv }[0]

header = nil

def wrap(list, splitby, wc)
	list.split(splitby).map{|x| "#{wc}#{x}#{wc}" }.join(", ")
end

tableName = "#tmp1"

i = 0
File.foreach(finput) do |line|
	i += 1
	line = line.strip
	if header == nil 
		header = line
		
		cols = line.split(",").map{|c| "[#{c}] varchar(500) " }.join(", ")
		puts "-- drop table #{tableName} "
		puts "set nocount on"
		puts "go"
		puts "create table #{tableName} ( #{cols} ) "
	else 
		# puts line
		vals = wrap(line, ",", "'")
		puts "insert into #{tableName} (#{header} ) values (  #{ vals } ) "
	end
	
	puts "go -- #{i}th " if i % 50 == 0
	
	
end

puts "-- Header: #{header}"
puts "select top 3 * from #{tableName} "
puts "select count(*) from #{tableName} "



