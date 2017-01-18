require 'net/http'
require 'fileutils'

SERVER_PORT = "http://10.241.40.161:7101/"	# .161 is PNWAPP1A
MOD_SHOW_TIMING = 1000

# get_mssg_doc_text 123
class MssgDocApi

	# 1st param is FILE with list of mssg_doc_ids (2nd column optional to be name of file in directory - use SQL to decide)
	# 2nd param is directory to write files.  If mssg_doc_id.txt exists
	def usage
		print "\n\nUsage: \n\n"
		print "ruby get_mssg_docs.rb filename_mssgdocids_filenames.txt c:\\toThisDir \n\n"
		exit
	end

	def get_mssg_doc_text mssg_doc_id
		server_port = SERVER_PORT
		path = "/sysmgmt/mssggrab_sitescope.jsp?mssgdocid=#{mssg_doc_id}"
		data = http_get server_port, path
	end

	def http_get server_port, path, debug = 0
		uri = URI.parse(server_port)
		http = Net::HTTP.new(uri.host, uri.port)
		response = http.request(Net::HTTP::Get.new(path))
		code = response.code
		data = response.body
		
		puts "HTTP Code: #{code} - #{data.size} for #{path}" if debug > 0
		
		data
	end

	def write_mssg_doc mssg_doc_id, out_dir, fn, skip = 0
		newfile = File.join(out_dir, fn)
		txt = (skip==0) ? 'BUT NOT' : ''
		if File.exists? newfile
			puts "#{newfile} already exists.  #{txt} Skipping." if skip > 0
			return if skip > 0
		end

		data = get_mssg_doc_text mssg_doc_id
		
		fout = File.open(newfile, "w")
		fout.write data
		fout.close
		
		data.size
	end

	def show_timing(t0, i, show = false) 
		if i < 10 || i % MOD_SHOW_TIMING == 0 || show
			ti = Time.now
			total = ti-t0
			avg = total / i
			puts "Processed #{i} records in #{ti - t0} seconds.  Avg/row: #{avg} "
		end
	end

end
