# https://www.hackerrank.com/challenges/chocolate-feast

t = gets.to_i
while t > 0
	# $n=money, c=cost-of-choc, m=wrappers needed for free chocolate
	n,c,m = gets.split(" ").map{|s| s.to_i }
	
	# initial purchase
	purchased = n / c
	
	# Wrappers can now be used iteratively ...
	wrappers = purchased
	while wrappers >= m
		extras = wrappers / m
		# puts "a) wrappers: #{wrappers} extras: #{extras} purchased: #{purchased} "
		
		wrappers -= extras * m	# used up this many wrappers
		wrappers += extras
		purchased += extras
		extras = 0
		
		# puts "b) wrappers: #{wrappers} extras: #{extras} purchased: #{purchased} "
	end
	
	puts purchased	
	# puts "n:#{n} c:#{c} m:#{m} => #{purchased} \n\n"
	
	t -= 1
end