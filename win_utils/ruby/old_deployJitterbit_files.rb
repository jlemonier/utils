# Deploy SQL Files specified by directories

require 'open3'

def snow; Time.now.strftime("%Y-%m-%d_%H-%M-%S"); end  # str of now
server = "qadb1b"
db = "JitterBit_dev"
output = File.open("#{server}_#{db}_#{snow}.output", "w")

def log(str)
	puts(str)
	output.puts(str)
end
def run_cmd(cmd) 
	log("Running command: #{cmd} at #{snow} ")
	stdin, stdout, stderr = Open3.popen3(cmd)
	log "	OUTPUT: #{stdout.read}"
	log "	ERROR:  #{stderr.read}"
end

sqldirs = []
# Orig Plus Logging
# sqldirs.push(%w{C:\code\gtnexus\development\modules\main\tradiant\release\sql\rel\jitterbit\proc\orig_plus_logging_only}[0] )

# Deploy Directories
sqldirs.push(%w{\\\\gthqfile1\engineering\docs\QA\PatchFiles\14.4.0\P1_Patches\P1_PSO-984-NDB1A_JitterBit_JasonL\Step1_setup_logging}[0] )
# sqldirs.push(%w{\\\\gthqfile1\engineering\docs\QA\PatchFiles\14.4.0\P1_Patches\P1_PSO-984-NDB1A_JitterBit_JasonL\Step2_add_logging}[0]   )

# Development
# sqldirs.push(%w{C:\code\gtnexus\development\modules\main\tradiant\release\sql\rel\jitterbit\proc}[0] )


sqldirs.each do |sqldir|
	puts "Processing files in: #{sqldir} at: #{snow} ..."

	# File.listfiles(sqldir).each do |f|
	Dir.entries(sqldir).each do |f|
	  f2 = File.join(sqldir, f)
	  if File.file? f2 and f =~ /\.sql$/
		puts f
		
		# system "echo Running #{f} on #{server} \ #{db} now to confirm ..."
		cmd = "sqlcmd -S #{server} -d #{db} -i #{f2} "
		run_cmd(cmd)
		
	  end
	end
end