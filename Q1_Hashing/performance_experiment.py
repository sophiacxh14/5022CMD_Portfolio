"""
performance_experiment.py
-------------------------
Experiment: compare SEARCH performance of the hash table (open addressing,
linear probing) against a one-dimensional array (linear search).

Fair-test design:
  * Both structures receive exactly the SAME records.
  * Both are searched for exactly the SAME keys, in the same order.
  * Each search batch is repeated several times and averaged to reduce noise.
  * The test is run at several data sizes to show how each structure scales.
"""

import random
import time
from typing import Any

from array_storage import ArrayStorage
from hash_table import HashTable
from medicine import Medicine

DATA_SIZES = [100, 1_000, 5_000, 10_000]   # number of records in each test
SEARCHES_PER_TEST = 1_000                  # searches in one timed batch
REPEATS = 5                                # each batch is repeated and averaged
RANDOM_SEED = 42                           # fixed seed = same "random" data every run
CATEGORIES = ["Pain Relief", "Antibiotic", "Allergy", "Supplement",
              "Cough & Cold", "Digestive", "Skin Care", "Respiratory"]


def generate_medicines(count: int, rng: random.Random) -> list[Medicine]:
    """Create `count` medicines with unique random product IDs."""
    product_ids = rng.sample(range(1_000, 10_000_000), count)   # no duplicates
    return [
        Medicine(product_id,
                 f"Test Medicine {product_id}",
                 rng.choice(CATEGORIES),
                 round(rng.uniform(1.0, 100.0), 2),
                 rng.randint(0, 500),
                 rng.random() < 0.3)                 # about 30% need a prescription
        for product_id in product_ids
    ]


def time_insert_all(storage: Any, medicines: list[Medicine]) -> int:
    """Insert every medicine into the storage and return the total time in ns."""
    start = time.perf_counter_ns()
    for medicine in medicines:
        storage.insert(medicine.product_id, medicine)
    return time.perf_counter_ns() - start


def average_search_time(storage: Any, keys: list[int]) -> float:
    """
    Search for every key, repeated REPEATS times.
    Return the average time for ONE search, in nanoseconds.
    """
    total_ns = 0
    for _ in range(REPEATS):
        start = time.perf_counter_ns()
        for key in keys:
            storage.search(key)
        total_ns += time.perf_counter_ns() - start
    return total_ns / (REPEATS * len(keys))


def run_experiment() -> None:
    rng = random.Random(RANDOM_SEED)

    print("=" * 78)
    print(" SEARCH PERFORMANCE: HASH TABLE (linear probing) vs ARRAY (linear search)")
    print("=" * 78)
    print(f" Each result = average time of ONE search, from {SEARCHES_PER_TEST:,} searches"
          f" x {REPEATS} repeats\n")

    print(f" {'Records':>8} | {'Search type':<15} | {'Hash Table':>12} | "
          f"{'Array':>14} | {'Hash Table is':>15}")
    print(" " + "-" * 76)

    for size in DATA_SIZES:
        medicines = generate_medicines(size, rng)

        # 1. Insert the SAME data into both structures
        table, array = HashTable(), ArrayStorage()
        table_insert_ns = time_insert_all(table, medicines)
        array_insert_ns = time_insert_all(array, medicines)

        # 2. Choose the SAME search keys for both structures
        existing_keys = [rng.choice(medicines).product_id for _ in range(SEARCHES_PER_TEST)]
        stored_ids = {medicine.product_id for medicine in medicines}
        missing_keys = []
        while len(missing_keys) < SEARCHES_PER_TEST:
            candidate = rng.randint(10_000_000, 20_000_000)   # outside the ID range
            if candidate not in stored_ids:
                missing_keys.append(candidate)

        # 3. Check both structures give the SAME answers (correctness first!)
        for key in existing_keys[:50] + missing_keys[:50]:
            assert table.search(key) is array.search(key), f"Mismatch for key {key}"

        # 4. Time the searches
        for label, keys in (("Found (random)", existing_keys),
                            ("Not found", missing_keys)):
            table_ns = average_search_time(table, keys)
            array_ns = average_search_time(array, keys)
            speedup = array_ns / table_ns
            print(f" {size:>8,} | {label:<15} | {table_ns:>9,.0f} ns | "
                  f"{array_ns:>11,.0f} ns | {speedup:>8,.1f}x faster")

        print(f" {'':>8} | {'(insert all)':<15} | {table_insert_ns / 1e6:>9,.2f} ms | "
              f"{array_insert_ns / 1e6:>11,.2f} ms |")
        print(f" {'':>8} | Final table: {table.capacity:,} slots, "
              f"load factor {table.load_factor:.2f}")
        print(" " + "-" * 76)

    print("\n Note: timings vary between computers and runs; the TREND is what matters.")


if __name__ == "__main__":
    run_experiment()