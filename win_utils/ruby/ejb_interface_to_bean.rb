require 'find'
require 'xmlsimple'
# hi

# C:\src\agile_13_7\test\properties\excel.properties
rootDir = "c:/src/agile_13_7/release" # .gsub("/","\\")

Dir["#{rootDir}/com/**/ejb-jar.xml"].each do |ex|
	
	begin
  	xhash = XmlSimple.xml_in(File.read(ex))
  	# se Is <session> or <entity>
  	eb = xhash['enterprise-beans'][0]
  	
  	if eb
      se = eb['session'] || eb['entity']
      se = se[0] if se
      remote, ejb = se['remote'][0], se['ejb-class'][0] if se rescue nil
      
      remote, ejb = se['local'][0], se['ejb-class'][0] if se && !remote rescue nil
  	end
  	
  	if not remote
      md = eb['message-driven']
      md = md[0] if md
      remote, ejb = md['ejb-name'][0], md['ejb-class'][0] if md
  	end

    if remote
      puts "# #{ex} - Parsed OK"
    	puts "#{remote}=#{ejb} \n\n"
    else
      puts "# #{ex} - Failed to Parse and determine interface=ejbbean OR remote=ejb"
      puts "####################### FAILED ########################################"            
    end  	

  rescue Exception => e
    puts e
    puts "#{ex} - Failed to parse! ************************************** "
    puts File.read(ex)
    puts "#{ex} - Failed to parse! ************************************** - END"
    
    raise e
  end	
	
	
end