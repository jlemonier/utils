Function Fib($n) {
    if ($n -lt 2) {
        return $n
    }
    return (Fib($n - 2)) + (Fib($n - 1))
}

Fib (22)