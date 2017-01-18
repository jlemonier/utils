
## Parse GTNx SO.xml for key fields

require 'rexml/document'
include REXML

folder = "./docs"
i = 0

fnout = "gap_output.csv"


def getTag root, tag
	result = ""
	XPath.each(root, "//#{tag}") { |e| result = e.text }
	result
end

data = ["mssg_doc_id", "filename","CommercialInvoiceNumber","ShippingOrderNumber","PurchaseOrderNumber"]
puts(data.join(","))

out = File.open(fnout, "w")
out.write(data.join(",") + "\r\n")

# Get Tags
Dir.entries(folder).each do |e|
	id,fn = e.split("_", 2)
	next if e.start_with?(".")
	i += 1
	puts "#{i}) #{e} "
	
	file = File.new(folder+"/"+e)
	doc  = REXML::Document.new file
	
	root = doc.root
	
	cinum 	= getTag(root, "CommercialInvoiceNumber")
	so 		= getTag(root, "ShippingOrderNumber")
	ponum 	= getTag(root, "PurchaseOrderNumber")
	
	data = [id, fn, cinum, so, ponum]
	puts(data.join(","))
	
	out.write(data.join(",") + "\r\n")
	
	# break if i > 10
end

out.close

def test2

	so = root.elements["ShippingOrder"]
	
	puts so
	puts so.attributes
	
	sonum = so.attributes["ShippingOrderNumber"]
	puts sonum
	
	cinum = so.elements["CommercialInvoiceNumber"]
	puts cinum
	puts cinum.text
	# XPath.each(doc, "//ShippingOrder") {|e| puts e }


end