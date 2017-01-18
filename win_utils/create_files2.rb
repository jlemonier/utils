require 'fileutils'
require 'securerandom'
## Make Unique files

PREFIX = %W(TiB GiB MiB KiB B).freeze

def as_size( s )
  s = s.to_f
  i = PREFIX.length - 1
  while s > 512 && i > 0
    i -= 1
    s /= 1024
  end
  ((s > 9 || s.modulo(1) < 0.1 ? '%d' : '%.1f') % s) + ' ' + PREFIX[i]
end

def hms
	Time.now.strftime("%Y%m%d%H%M%S")
end

def random_data(size)
	# SecureRandom.random_bytes(size)	# Creates binary data that cannot be viewed easily in most editors.
	SecureRandom.hex(size / 2)			# Creates hex data: 0-9 and a-f only but still random.  Easy to view in text editor
end


def create_file(root_dir, filename, size)
	fn = File.join(root_dir, filename)
	File.open(fn, 'w') { |file| file.write(random_data(size)) }
end

def create_files(root_dir, num_files, size)
	batch_dir = File.join(root_dir, hms)
	FileUtils.mkdir_p(batch_dir)
	
	print "In Directory for batch: #{batch_dir}, creating #{num_files} files of size: #{as_size size}  \n"
	(1..num_files).each do |n|
		# print "Creating file: #{n} in #{batch_dir} \n"
		create_file(batch_dir, "file_#{n}", size)
	end
end

default_filesize = 1024*2
# default_filesize = 1024^2

root_dir  = ARGV[0] || "???"
num_files = (ARGV[1] || 1000).to_i
size = (ARGV[2] || (default_filesize)).to_i
size2 = as_size(size)

total = num_files * size
total2 = as_size(total)


print "\n\nUsage: ruby create_files.rb START_DIR, NUM_FILES, SIZE_PER_FILE\n\n"
exit if root_dir.match(/\?\?\?/)

print "In Directory: #{root_dir}, creating #{num_files} files of size: #{size2} for total space of: #{total2} \n"

create_files(root_dir, num_files, size)


