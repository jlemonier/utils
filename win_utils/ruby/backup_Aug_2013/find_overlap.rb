# Find tasks running 
require 'csv'
require './task'

# 8-1
src_file = "d:/gt/projects/Aug_2013_Perf_Duplicate_Check/Aug_2013_Performance_Duplicate_Task_check_sorted_noExceptions.csv"

# 8-20
src_file = "d:/gt/projects/Aug_2013_Perf_Duplicate_Check/Aug_20_2013_Performance_Duplicate_Task_check_sorted_noExceptions.csv"

# Exceptions have newlines!!
#File.open(src_file).each_with_index do |l,i|
#	print "#{i}) #{l} \n" if i % 1000 == 0
#end

i = 0
prevTask = Task.new({})
prevKey = "XUZZZXXX"
seqMatches = 0
minTime = nil
maxTime = nil

overlaps = 0

def min(a, b)
	return b if not a
	return a if not b
	return (a < b) ? a : b
end

def max(a, b)
	return b if not a
	return a if not b
	return (a > b) ? a : b
end

CSV.foreach(src_file, :headers => true) do |curRow|
	curTask = Task.new(curRow.to_hash)
	i += 1
	
	minTime = min(minTime, curTask.starttime)
	maxTime = max(maxTime, curTask.endtime)
	
	curKey = curTask.key
	if curKey == prevKey
		seqMatches += 1
		# print "Found #{curKey} #{seqMatches} times in a row \n"
	
		# Now check for overlaps
		overlaps += curTask.print_overlap_info (prevTask)
	else
		seqMatches = 0
	end
	
	prevTask = curTask
	prevKey  = prevTask.key
	xshow = 1000
	print "\n\nShowing every #{xshow}th row - #{i}) #{curRow.to_hash.values.join(" || ")} \n\n" if i % xshow == 0
	
end

print "\n\nFound #{overlaps} overlapping tasks starting from: #{minTime} and ending to #{maxTime} over #{i} records."


"""


"""