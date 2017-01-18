print "__ENCODING__=#{__ENCODING__} in convert2utf8.rb \n" 
# Ruby program to walk a directory and convert every file to utf-8

files = Dir['e:/apps/utils/ruby/artifacts/**/*.*']

fnum = 0
files.each do |fn|
  fnum += 1
  File.open(fn, 'r:utf-8') do |f|
    puts "#{fnum}) #{fn} file .external_encoding.name: #{f.external_encoding.name} "
	# content = f.read
	# puts "\t\tContent: bytes=#{content.size} encoding: #{content.encoding.name} "
	
  end
end

