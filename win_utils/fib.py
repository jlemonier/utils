# Implement caching version of Fib for Python / Powershell / Ruby

import time

class Fib:
    def __init__(self):
        self.fib_cache = {}
        self.cache_flag = 1
        
    def set_cache_flag(self, flag = 1):
        self.fib_cache = {}
        self.cache_flag = flag
        
    def run_fib(self, n):
        start = time.time()
        # Iteratively (not recursively) do all the work first, then continue.
        # Or fib(40000) blows up stacktrace
        # Similar to following sequence:
        # 1 1 2 3 5 8 ... n in increasing order.
        if (self.cache_flag > 0):
            if (n > 5 and  not self.get(n)):
              for i in range(3, n):
                # print ("Calling fib(%s) now for setup "%(i))
                self.fib(i)
        
        result = self.fib(n)
        end = time.time()
        print("fib(%s)=%s in: %.2f seconds - Caching: %s"%(n, result, (end-start), self.cache_flag) )
        return result
        
    def cache(self, n, result):
        if (self.cache_flag > 0):
            self.fib_cache[n] = result
            
    def get(self, n):
        return self.fib_cache.get(n)
        
    def fib(self, n, step = "*"):
        if (n < 0):
            return 0
        if (n < 2):
            return n
            
        if self.cache_flag > 0:
            result = self.get(n)
            if result > 0:
                # print ("%s) fib: %s Cached! => %s"%(step, n, result))
                return result

        # print ("%s) fib: %s NOT YET cached? => %s"%(step, n, result))

        # print ("Cache: %s" %(self.fib_cache))
        # print self.fib_cache
        # keys = " ".join(self.fib_cache.keys())
        # cached = self.fib_cache.get(n)
        
            
        step2 = step + "*"
        result = self.fib(n-1, step2) + self.fib(n-2, step2)
        # self.fib_cache[n] = result
        self.cache(n, result)
        # print ("Caching: fib(%s) => %s now."%(n, result))
        return result

f = Fib()        
# for i in range(-5,100):
#   f.run_fib(i)

# RuntimeError: maximum recursion depth exceeded in cmp

# Test timing ...
for i in range(1,300000):
    f.set_cache_flag(1)
    f.run_fib(i)

    if i < 30:    # or too slow
        f.set_cache_flag(0)
        f.run_fib(i)



    