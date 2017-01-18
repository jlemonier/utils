# Ruby program that runs html2haml
#  parameters:
#   @dir
#   @recurse

require 'find'

pdir = ARGV[0]
precurse ||= ARGV[1] || false

Find.find(pdir) do |f|
  if f.match /\.erb\Z/
  	f2 = f.name.gsub /\.erb\Z/.haml/
  	puts "Found erb file: #{f} => #{f2} "
  end
end