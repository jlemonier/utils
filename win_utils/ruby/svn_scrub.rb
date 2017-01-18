# Ruby Utility to remove SVN-keywords and scrub code for comparing SVN vs. GIT
require 'fileutils'
require 'optparse'
require 'yaml'
require 'find'
require 'pathname'
# require 'ptools' # binary or text ?

class SvnScrub
	attr_accessor :src, :dest, :count

	def initialize src, dest
		@src = src
		@dest = dest
		@count = 0
	end
	
	def process
		puts src
		puts File.exists? src
		if not File.exists? src
			puts "#{src} directory does not exist.  Skipping. "
			return
		end
	
		# Walk entire src ... for each file, copy to dest after scrubbing
		n = 0
		srcparent = src.split(/\\|\//)[-1]
		puts "src: #{srcparent} <= #{src} "
		
		Find.find(src) {|fn|
			# Skip unneeded files for diff
			next if fn =~ /#{srcparent}\/\.svn/
			next if fn =~ /#{srcparent}\/bin/
			next if fn =~ /#{srcparent}\/build/
			next if fn =~ /#{srcparent}\/docs/
			
			n += 1
			scrub_and_copy(fn)
			
			# break if n > 100
			puts ("\n\n\nAt: #{n}th file now ... \n\n\n") if n % 100 == 0
		}
	end

	def scrub_and_copy fn
		return if File.directory? fn
		@count += 1
		
		puts ("#{count}) #{fn} ... (scrub_and_copy)") if count % 1000 == 0
		newfn = fn.gsub(src, dest)
		newdir = File.dirname(newfn)
		FileUtils.mkdir_p(newdir) rescue puts "Failed to create dir: #{newdir} "
		
		if binary_ext?(fn)
			# mklink newfn, fn
			copy_file fn, newfn
		else
			File.open(newfn, "w") {|out| File.open(fn).each {|line| out.write(scrub(line)) } }
		end
	end
	
	# Check timestamp first
	def copy_file fn, newfn
		if File.exists?(newfn) and File.mtime(newfn) == File.mtime(fn)
			puts "Skipping copy to: #{newfn} - exists with same modtime" 
		else
			puts "Copying #{newfn} ..." 
			FileUtils.cp(fn, newfn)
		end
	end
	
	# TODO - couple attempts with utilities failed?
	def binary_ext? fn
		return true if fn =~ /\.jar$|\.png$|\.jpg/i ;
		return false
	end

	# hmmm worked fine from command line.  Maybe an Admin subshell is not Admin anymore?  another spawned cmd.exe shell ?
	def mklink newfn, fn
		newfn = newfn.gsub("/", "\\")
		fn    = fn.gsub("/", "\\")
		puts "Linking binary file: #{fn}\n 	to	#{newfn} "
		cmd = "mklink #{newfn} #{fn}"
		puts cmd
		exec cmd	# hmmm worked fine from command line.  Maybe an Admin subshell is not Admin anymore?  another spawned cmd.exe shell ?

	end

	# $Id: ... $
	# $Revision: ... $
	# non-greedy match $XYZ:...$  $AbC:...$ ==> $XYZ$ $AbC$
	def scrub line
		# line = line.gsub(/\$Id:.*?\$/, "$Id$")
		# line = line.gsub(/\$Revision:.*?\$/, "$Revision$")
		line2 = line.gsub /\$([A-Za-z-]+):.*?\$/, '$\1$'
		print "\n\tScrubbed SVN Keywords: #{line2.rstrip} <<== #{line.rstrip} " if not line.eql?(line2)
		line2
		
		# GIT has unix \n only, not \r\n
		# line = line.gsub /\r\n/, "\n" 	# WinMerge ignores line-endings just fine, DiffMerge did not
	end
	
	def run_tests
		scrubs = []
		scrubs << "	static final String __cvsid = \"$Id: MssgConfigDaoImpl.java  2013-08-18 17:04:11Z vsalian $\"; "
		scrubs << " exec tp_dbbeginscript '$Id$Id: tz_intaudit_msgid_dml_15632.sql 190473 2011-12-15 05:35:38Z harini $'; "
		
		scrubs.each {|s| puts "Testing line ... \n1) #{s} \n2) #{scrub(s)}" }
	end
end
