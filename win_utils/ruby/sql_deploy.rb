# Deploy SQL Files specified by directories

require 'open3'
SEP = File::SEPARATOR

class SqlDeploy
	# Defaults to "make the scripts for deploy"
	def initialize server, db, run_cmds = false, log_cmds = true, pause = true	# log_cmds == "Create script with commands to run"
		@server = server
		@db     = db
		@sqldirs = []
		@log_cmds = log_cmds
		@run_cmds = run_cmds
		@pause    = pause
		Dir.mkdir("log") unless File.exists?("log")
	end
	# Happens upon deploy call, not init (so deploy_jitterbit.rb doesn't make extra blank files)
	def setup_output
		@output      = File.open(File.join("log", "#{@server}_#{@db}_#{snow}.output"), "w")		if @run_cmds
		@output_cmds = File.open(File.join("log", "#{@server}_#{@db}_#{snow}.cmd"), "w")		if @log_cmds	
	end
	
	def add_dir xdir
		@sqldirs.push xdir
	end
	# @server = "qadb1b"
	# @db = "JitterBit_dev"

	def snow; Time.now.strftime("%Y-%m-%d_%H-%M-%S"); 	end  # str of now
	def log(str, extra_blank = false)
		puts(str)
		# @output_cmdsoutput.puts(str)
		
		if extra_blank
			puts "" 
			@output.puts "" 
		end
	end

	def run_cmd(cmd) 
		@output_cmds.puts(cmd) if @log_cmds
	
		if @run_cmds
			log("\nRunning command: #{cmd} at #{snow} ")
			begin
				stdin, stdout, stderr = Open3.popen3(cmd)
				log "	OUTPUT: #{stdout.read}"
				log "	ERROR:  #{stderr.read}"
			rescue => e
				log "	OUTPUT: "
				log "	ERROR: #{e} "
			end
		end
	end

	def deploy
		setup_output
	
		@sqldirs.each do |sqldir|
		
			if not File.directory? sqldir
				log("\nDirectory not valid: #{sqldir} - skipping.")
				next
			end
			log "\nProcessing files in: #{sqldir} at: #{snow} ... \n\n"

			files = Dir.entries(sqldir).sort_by {|x| x}
			files.each do |f|
			  f2 = File.join(sqldir, f)
			  if File.file? f2 and f =~ /\.sql$/
				# puts f				
				# system "echo Running #{f} on #{server} \ #{db} now to confirm ..."
				cmd = "sqlcmd -S #{@server} -d #{@db} -i #{f2} "
				run_cmd(cmd)
			  end
			end
		end
		
		if @run_cmds
			log "\nResults: #{File.realpath @output}" 
			@output.close
		end

		if @log_cmds
			log "\nCommands Logged: #{File.realpath @output_cmds}"
			
			if @pause
				@output_cmds.puts("echo \"JitterBit code deployed.  pause added at bottom of script to check for errors in console\" ")
				@output_cmds.puts("pause")
			end
			@output_cmds.close
		end
		
	end
end
