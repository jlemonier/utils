require 'net/http'
require 'fileutils'
require './mssg_doc_api'

# get_mssg_doc_text 123

def usage stop = true
	puts "Usage - Get Files From MssgServer"
	puts "	ruby get_mssg_docs.rb <filename.csv> <output directory>"
	puts "	 <filename.csv> 1st column must be: mssg_doc_id"
	puts "	 <filename.csv> 2nd column must be: filename you wish to name the file."
	puts """ SQL Tip for pdb1a.mssg_newtradmarket

	select top 50 mssg_doc_id
		, filename+'_'+cast(mssg_doc_id as varchar) filename
	from tt_mssg_doc_NEW	-- tt_mssg_doc is now a view so 
	where createtime > getdate() - 1
	order by createtime desc, mssg_doc_id desc

		"""
	
	abort "Ruby Program stopped because reuqired parameters are missing" if stop
	
end

mdapi = MssgDocApi.new	
	
fn_ids = ARGV[0]	# See Usage - 1st param is filename with list of mssg_doc_ids 1st column and filename_desired 2nd column
out_dir = ARGV[1]	# See Usage - 2nd param is output directory
usage if fn_ids.to_s.size < 1
usage if out_dir.to_s.size < 1

FileUtils.mkdir_p out_dir

t0 = Time.now

i = -1
total_bytes = 0
File.open(fn_ids).each do |line|
	i += 1
	next if i < 1
	# print line
	id, fn = line.split(",")
	# fn = "#{fn}.txt"
	
	id = id.strip
	fn = fn.strip

	fn = id if fn.to_s.size < 1
	fn = "#{fn}.txt" if not fn =~ /\./
	
	if File.exists?("#{out_dir}/#{fn}") 
		print "Skipping mssg_doc_id=#{id} - file exists already: #{out_dir}/#{fn} \n"
		next
	else
		print "Getting mssg_doc_id=#{id} and saving as: #{out_dir}/#{fn} \n"

		bytes = mdapi.write_mssg_doc(id, out_dir, fn)
		total_bytes += bytes
		
		mdapi.show_timing(t0, i)		
	end
end

mdapi.show_timing(t0, i, true)
puts "#{i} files with total bytes: #{total_bytes}"