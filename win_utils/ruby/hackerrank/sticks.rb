# https://www.hackerrank.com/challenges/cut-the-sticks
# Enter your code here. Read input from STDIN. Print output to STDOUT
i1 = nil # || "6"
i2 = nil # || "5 4 4 2 1 8"

sticks = (i1 || gets).to_i
info   = (i2 || gets).to_s.split(" ").map(&:to_i)

while info.size > 0
	puts info.size
	shortest = info.min

	info = info.map{|i| i - shortest}.select{|i| i > 0}
end
