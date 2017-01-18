require 'net/http'
require 'fileutils'
require './mssg_doc_api'

SERVER_PORT = "http://10.241.40.161:7101/"	# .161 is PNWAPP1A
MOD_SHOW_TIMING = 1000

# get_mssg_doc_text 123

mdapi = MssgDocApi.new	
	
fn_ids = ARGV[0]	# See Usage - 1st param is list of mssg_doc_ids
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
	fn = id if fn.to_s.size < 1
	fn = "#{fn}.txt" if not fn =~ /\./
	
	id = id.strip
	fn = fn.strip
	
	print "Getting mssg_doc_id=#{id} and saving as: #{out_dir} \ #{fn} \n"
	
	bytes = mdapi.write_mssg_doc(id, out_dir, fn)
	total_bytes += bytes
	
	mdapi.show_timing(t0, i)
end

mdapi.show_timing(t0, i, true)
puts "#{i} files with total bytes: #{total_bytes}"