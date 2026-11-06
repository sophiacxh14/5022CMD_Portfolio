# 5022CMD Advanced Algorithms – Portfolio

**Student:** Sophia Chan Xin Hui (INTI: P24016371 | CU: 17955948)
**Module:** 5022CMD Advanced Algorithms – Individual Report (August 2026)

This repository contains the Python source code for the three programs in the portfolio.

## Requirements

- Python 3.10 or newer
- No external libraries are needed (only Python's built-in `random`, `time`, `os` and `threading` modules)

## Repository structure

| Folder | File to run | Description |
|---|---|---|
| `Q1_Hashing/` | `pharmacy_inventory.py` | Pharmacy Inventory System using a hash table with open addressing and linear probing |
| `Q2_Graph/` | `course_prerequisites.py` | University Course Prerequisite System using an unweighted directed graph |
| `Q3_Concurrency/` | `fibonacci_threads.py` | Fibonacci(35), (38) and (40) calculated with and without multithreading |

## How to run

Open the folder in a terminal (or in PyCharm) and run the file, for example:

```
python Q1_Hashing/pharmacy_inventory.py
```

## Features

### Question 1 – Hashing
- Hash table using open addressing with linear probing, tombstones for deletion and automatic resizing (prime table sizes, load factor below 0.7)
- `Medicine` entity class with 15 pre-defined records
- Menu: insert, search, edit, delete, view all products and view the hash table slot layout
- Performance experiment comparing hash table search with linear search in a one-dimensional array (menu option 7)

### Question 2 – Graph
- Generic directed graph stored as an adjacency list (`add_vertex`, `add_edge`, `remove_edge`, `list_incoming_adjacent_vertex`, `list_outgoing_adjacent_vertex`)
- `Course` entity class with 8 pre-defined courses and their prerequisites (maximum 10 courses)
- Mandatory features: view all courses, view course details, view prerequisites, view courses unlocked
- Advanced features: course profile (electives show name only), add a course, add a prerequisite (with prerequisite-loop detection using depth-first search), remove a prerequisite

### Question 3 – Concurrent Processing
- Recursive Fibonacci function
- Multithreaded experiment: one thread per Fibonacci number, timed in nanoseconds over 10 rounds
- Sequential experiment over 10 rounds, followed by a comparison of the average times
- Note: the full experiment takes several minutes to complete