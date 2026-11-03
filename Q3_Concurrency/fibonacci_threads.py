"""
Question 3: Concurrent Processing - Fibonacci with and without Multithreading
==============================================================================
Calculates Fibonacci(35), Fibonacci(38) and Fibonacci(40):
  1. using multithreading (one thread for each number), and
  2. without multithreading (one number after another),
then compares the time taken in nanoseconds over several rounds.

Run this file to start the experiment.
"""

import time

# ---------------------------------------------------------------------------
# Settings (change them here, not inside the code)
# ---------------------------------------------------------------------------
FIBONACCI_NUMBERS = [35, 38, 40]   # the three Fibonacci numbers to calculate
ROUNDS = 10                        # number of rounds for each experiment


# ===========================================================================
# 1. FIBONACCI FUNCTION
# ===========================================================================
def fibonacci(n):
    """Return the nth Fibonacci number using recursion: F(n) = F(n-1) + F(n-2)."""
    if n <= 1:                                   # base cases: F(0) = 0 and F(1) = 1
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)   # each call makes two more calls


# ---------------------------------------------------------------------------
# Quick test: check the results and see how the time grows as n increases
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    first_eleven = []
    for n in range(11):
        first_eleven.append(fibonacci(n))
    print("F(0) to F(10):", first_eleven)

    for n in [20, 25, 30]:
        start = time.perf_counter_ns()
        result = fibonacci(n)
        elapsed = time.perf_counter_ns() - start
        print(f"F({n}) = {result:,}  took {elapsed:,} ns")