# Enter your code here. Read input from STDIN. Print output to STDOUT
T = gets.to_i
for t in 1..T 
    in_nk = gets.to_s
    students = gets.to_s.split(" ").map{|s| s.to_i}
    ontime = students.select{|s| s <= 0}.count
    
    n,k = in_nk.split(" ").map{|s| s.to_i}
    
    puts ontime < k ? "YES" : "NO"
    
end
