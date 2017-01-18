# https://www.hackerrank.com/challenges/caesar-cipher-1

letters = gets.to_i
input   = gets
kmove   = gets.to_i

puts input

lower = ["a".."z"]
upper = ["A".."Z"]

puts lower.to_s

for c in input.chars
  # #{(c.to_s.ord +1).to_s }
  puts "#{c} #{c.next.next} #{((c.ord)+2).chr}  "
end