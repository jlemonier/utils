# Usage:
# ruby scrub.rb -p paths.txt
#  Each path will be scrubbed to:  path__scrubbed

# Ruby Utility to remove SVN-keywords and scrub code for comparing SVN vs. GIT
require 'fileutils'
require 'optparse'
require 'yaml'
require 'find'
# require 'ptools' # binary or text ?

require './svn_scrub'

options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: example.rb [options]"
  opts.on('-p', '--paths NAME', 'paths')	{ |v| options[:paths] = v 	}
end.parse!

def usage
	puts "\nPurpose: "
	puts "  QA of SVN->GIT migration.   "
	puts "  Checkout 2 repos, strip svn-keyword content for comparison: $Id: LocationDAO.java 240400 2013-08-26 14:06:46Z bbanagude $ ==>> $Id$ "
	puts ""
	puts "Usage: "
	puts "  ruby scrub.rb -p paths.txt"
	puts "    Paths.txt has 1-line per <dir> to scrub. "
	puts "    Copies to <dir>__scrubbed.  Leaves <dir> alone. "
	puts ""
end

files = File.open(options[:paths]).readlines
usage
puts "Script options: #{options} "
puts files
# puts "ARGV: #{ARGV} "

files.each do |src|
	src = src.strip
	dest = src + "__scrubbed"

	# exec "title Scrubbing #{src} now ... "
	ss = SvnScrub.new(src, dest)
	
	puts "About to scrub: #{src} to #{dest} ... "
	ss.process
	
	ss.run_tests
end

