# ruby col2array.rb GAP_9400_invoice_lookups_all.csv 4 > gap_ponums.txt
# mssg_doc_id,filename,CommercialInvoiceNumber,ShippingOrderNumber,PurchaseOrderNumber,om_po_id,failed_inv?
# 5841947144,FTL.GTNEXUS.xml8.xml,510218077,510218077,VL8EINA
# 5841947149,FTL.GTNEXUS.xml5.xml,510218074,510218074,VL8ECNA
# 5841947158,FTL.GTNEXUS.xml1.xml,510218070,510218070,VL8EFNA
# ==>> 'VL8EINA','VL8ECNA', ...


if ARGV.size < 2
	print "Usage        : ruby col2array.rb $filename $colnum $delim \n"
	print "Usage Example: ruby col2array.rb filename.txt 3 , \n"
	exit
end

fn = ARGV[0]
colnum = ARGV[1].to_i
delim = ","

list = []
IO.foreach(ARGV[0]) do |line|
	line = line.strip
	x = line.split(delim)
	# print "#{x} \n"
	list << x[colnum]
end

result = list.map{|e| "'#{e}'" }.join(delim)
print "#{result} \n"

