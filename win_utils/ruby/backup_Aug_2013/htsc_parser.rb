# D:\gt\projects\HTSC_Fix_Aug_2013\test_3.csv
# D:\gt\projects\HTSC_Fix_Aug_2013\test_3
require 'xmlsimple'
require "awesome_print"		# VERY nice tool for showing Ruby hashes & arrays in readable form

# Now we can require this file and use this class easily without bothering to store XML files at all

# def get_htsc_fix_results text, header = []
class HtscParser

	def print_csv cols
		puts "#{cols.join(",")}"
	end

	""" XML:
	<References>
		<Type>Size</Type>
		<Value>690</Value>				</References>
	<References>
		<Type>Color</Type>
		<Value>MULTI/MULTI/</Value>		</References>
	<References>
		<Type>Dimension</Type>
		<Value>11-</Value>
		
	XML Simple parses to array:  (Removed quotes from here to preserve comment)
			References => [
		[0] {
			 Type => [
				[0] Size
			],
			Value => [
				[0] 690
			]
		},
		[1] {
			 Type => [
				[0] Color
			],
			Value => [
				[0] MULTI/MULTI/
			]
		},
	"""
	def get_type_values_as_hash xhash
		tvhash = {}
		xhash.each do |ref|
			type = ref['Type'][0]
			val  = ref['Value'][0]
			tvhash[type] = val
		end
		tvhash
	end

	# This function will return AN ARRAY of ARRAYS.
	# 1 XML file can have 3 lines, each with 4 assortnments, each with 2 HTSC codes => 24 rows for a single file
	# Pass in header with mssg_doc_id, createtime, etc. so this can be connected/written with each row
	def get_htsc_fix_results text, header = []
		results = []	# List of array/csv rows 
		
		xhash = XmlSimple.xml_in(text)		# Parse TEXT/XML into Ruby Arrays & Hashes
		# puts xhash['Order']				# See one chunk of parsed object
		# ap xhash							# "awesome_print" helps see Ruby object
		
		# We will denormaize from: Header => Lines => Assortment => HTSC.  As each loop occurs, we will dup array of fields and print when done
		header << xhash['Order'][0]['Header'][0]['OrderNumber']

		# <Order> <Details> ... then list of <LineItem> -- [0] are because Ruby XmlSimple makes them arrays because it is not looking at XSD
		lines = xhash['Order'][0]['Details']	# NO [0] here because we want the array not the hash of first LineItem
		lines.each do |li|
			line = header.dup
			line << li['LineItem'][0]['LineItemNumber']		# Add to array
			line << li['LineItem'][0]['ProductCode']
			
			assortments = li['LineItem'][0]['Assortment']
			# puts assortments	# Helps A LOT to print piece of Ruby Object (hashes & arrays) parsed by XmlSimple
			assortments.each do |asmt|
				asmtline = line.dup
				
				# Size / Color / Dimension are in array of References.  Get them as simple hash and append in order to array/csv
				asmt_references = get_type_values_as_hash(asmt['References'])
				['Size','Color','Dimension'].each {|attr| asmtline << asmt_references[attr] }
				
				# May have 2+ Harmonzied Codes per Assortment
				hcline = asmtline.dup
				harmcode_references = get_type_values_as_hash(asmt['HarmonizedCodeInfo'][0]['References'])
				['HTS','CustomsHTSText','UserDefChar1','UserDefChar2'].each {|attr| hcline << harmcode_references[attr] }
				
				# print_csv hcline
				
				results << hcline
			end
		end
		results
	end
end

