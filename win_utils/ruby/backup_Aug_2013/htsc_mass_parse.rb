# Loop through mssg_doc_ids, get text, parse text, write CSV file

require "./htsc_parser.rb"
require "./mssg_doc_api.rb"

mdapi = MssgDocApi.new	
hp 	  = HtscParser.new
	
fn_ids = ARGV[0]	# See Usage - 1st param is list of mssg_doc_ids AND ALL METADATA COLUMNS
out_dir = ARGV[1]	# See Usage - 2nd param is output directory
mdapi.usage if fn_ids.to_s.size < 1
mdapi.usage if out_dir.to_s.size < 1

FileUtils.mkdir_p out_dir
t0 = Time.now

fout = File.open(File.join(out_dir), "htsc_mass_parse_results.csv", "w")

i = -1
total_bytes = 0
total_htsc  = 0
File.open(fn_ids).each do |line|
	begin
		i += 1
		next if i < 1	# Skip header
		
		header = line.split(",")	# ALL rows in CSV line selected from MssgBus
		id = header[0].strip
		
		mssg_document_text = mdapi.get_mssg_text mssg_doc_id
		rows = hp.get_htsc_fix_results mssg_document_text, header
		
		# Write 1+ rows for each: PO - Line - Assortment - HTSC per PO.xml file
		total_htsc
		rows.each {|r| fout.write("#{r.join(",") } " ) }
		
		mdapi.show_timing(t0, i)
	rescue Exception => e
		puts e.message
		puts e.backtrace.inspect
	end
end

mdapi.show_timing(t0, i, true)
puts "#{i} files with total bytes: #{total_bytes}"

fout.close