# Enter your code here. Read input from STDIN. Print output to STDOUT
result = 1
n = gets.to_i
for i in 1..n
    result *= i
end
print result