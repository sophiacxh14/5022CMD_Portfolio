"""
Question 3: Concurrent Processing - Fibonacci with and without Multithreading
==============================================================================
Calculates Fibonacci(35), Fibonacci(38) and Fibonacci(40):
  1. using multithreading (one thread for each number), and
  2. without multithreading (one number after another),
then compares the time taken in nanoseconds over several rounds.

Run this file to start the experiment.
"""

import os
import threading
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


# ===========================================================================
# 2. WITH MULTITHREADING (one thread for each Fibonacci number)
# ===========================================================================
def fibonacci_task(n, index, results, start_times, end_times):
    """The work done by ONE thread: calculate F(n) and record when it started and finished.
    Each thread writes only to its own position (index) in the shared lists."""
    start_times[index] = time.perf_counter_ns()    # high-precision timer in nanoseconds
    results[index] = fibonacci(n)
    end_times[index] = time.perf_counter_ns()


def run_round_with_threads():
    """Calculate all the Fibonacci numbers at the same time, in separate threads.
    Returns the results and the time taken (ns)."""
    count = len(FIBONACCI_NUMBERS)
    results = [0] * count          # one position for each thread's answer
    start_times = [0] * count      # when each thread started
    end_times = [0] * count        # when each thread finished
    # Each thread only writes to its own index, so threads never overwrite each other (no race condition)

    threads = []
    for index in range(count):
        # target = the function the thread runs, args = the values passed to that function
        thread = threading.Thread(target=fibonacci_task,
                                  args=(FIBONACCI_NUMBERS[index], index, results, start_times, end_times))
        threads.append(thread)

    # Note: because of Python's Global Interpreter Lock (GIL), only one thread runs Python code
    # at a time, so the threads take turns (concurrent) instead of running in parallel.
    for thread in threads:
        thread.start()             # start every thread
    for thread in threads:
        thread.join()              # wait until every thread has finished

    # Time_Elapsed = End_Time_Of_Thread_Finished_Last - Start_Time_Of_Thread_That_Started_First
    elapsed = max(end_times) - min(start_times)
    return results, elapsed


# ===========================================================================
# 3. WITHOUT MULTITHREADING (one Fibonacci number after another)
# ===========================================================================
def run_round_without_threads():
    """Calculate the Fibonacci numbers one after another in the main program.
    Returns the results and the time taken (ns)."""
    results = []
    start = time.perf_counter_ns()
    for n in FIBONACCI_NUMBERS:
        results.append(fibonacci(n))
    elapsed = time.perf_counter_ns() - start
    return results, elapsed


# ===========================================================================
# 4. RUNNING THE EXPERIMENT
# ===========================================================================
def run_experiment(title, run_round):
    """Run one experiment for ROUNDS rounds, print the time of each round and return the average.
    run_round is the function that performs one round (with or without threads)."""
    print(f"\n=== Fibonacci Computation ({title}) ===")
    total = 0
    for round_number in range(1, ROUNDS + 1):
        results, elapsed = run_round()
        total += elapsed

        answers = []
        for index in range(len(FIBONACCI_NUMBERS)):
            answers.append(f"Fib({FIBONACCI_NUMBERS[index]})={results[index]}")
        # >15, right-aligns the time in 15 characters and adds commas between thousands
        print(f"Round {round_number:>2}: {', '.join(answers)} | T = {elapsed:>15,} ns")

    average = total / ROUNDS
    print(f"Average T ({title}): {average:,.0f} ns")
    return average


# ===========================================================================
# 5. MAIN PROGRAM
# ===========================================================================
def main():
    print(f"Calculating Fibonacci {FIBONACCI_NUMBERS} for {ROUNDS} rounds in each experiment.")
    print(f"This computer has {os.cpu_count()} CPU cores.")     # cores available for parallel work
    print("This can take several minutes, please wait...")

    threaded_average = run_experiment("With Multithreading", run_round_with_threads)
    sequential_average = run_experiment("Without Multithreading", run_round_without_threads)

    # Compare the two averages as a percentage of the time without threads
    difference = (threaded_average - sequential_average) / sequential_average * 100
    print("\n=== Comparison ===")
    print(f"Average T (With Multithreading)   : {threaded_average:>18,.0f} ns")
    print(f"Average T (Without Multithreading): {sequential_average:>18,.0f} ns")
    if difference > 0:
        print(f"Observation: Multithreading was {difference:.1f}% SLOWER than running without threads.")
    else:
        # -difference turns the negative percentage into a positive number for display
        print(f"Observation: Multithreading was {-difference:.1f}% FASTER than running without threads.")


# Run the experiment only when this file is executed directly, not when it is imported.
if __name__ == "__main__":
    main()