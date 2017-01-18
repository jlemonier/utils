Dir['**/*.*'].each do |f|
  print "call iso2utf8 \"#{f}\" \n" if File.file? f
end