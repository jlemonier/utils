require 'find'
require 'fileutils'

def make_batch batch, destdir, i
  batchdir = File.join(destdir, "batch_#{i}")
  FileUtils.makedirs(batchdir) if not File.exists? batchdir
  puts "Creating: #{batchdir}"
  batch.each_with_index do |bf, bi| 
    newfile = File.join(batchdir, File.basename(bf))
    puts("#{bi} - Copying #{bf} to: #{newfile} ") if bi % 200 == 0
    FileUtils.copy_entry(bf, newfile) if not File.exists? newfile
  end

end

def create_batches srcdir, destdir, batch_size
  
  batch_size = 2000 if batch_size <= 1
  batch = []
  i = 0
  Find.find(srcdir).each do |f|
    next if not File.file? f
    i += 1
    # puts "#{f}"
    batch << f
    
    if batch.size == batch_size
      make_batch(batch, destdir, i)      
      batch = []
    end
  end

  make_batch(batch, destdir, i) if batch.size > 0

end

batch_size = ARGV[0].to_i || 2000
# Need to get files in batches of 2000
by_customer = %w{C:\apps\by_customer_test\Extracted_Here\by_customer}[0]
by_customer = %w{H:\CE_Update_Object_Fix\Sep18\by_customer}[0]

by_cust_batches = %w{C:\apps\by_customer_test\Extracted_Here\by_customer_batchsize_}[0]
by_cust_batches = %w{H:\CE_Update_Object_Fix\Sep18\by_customer_batchsize_}[0]

by_cust_batches += "#{batch_size}"
puts "#{by_customer} / #{by_cust_batches}"

custi = 0
Dir.entries(by_customer).each do |custcode_dir|
  next if custcode_dir =~ /\.+/
  next if not custcode_dir =~ /ICVAN1/ 
  
  custi += 1
  # break if custi > 1
  puts "#{custcode_dir}" 
  
  srcdir = File.join(by_customer, custcode_dir)
  destdir = File.join(by_cust_batches, custcode_dir)
  FileUtils.makedirs(destdir) if not File.exists? destdir
  
  create_batches srcdir, destdir, batch_size 
  
  
end
