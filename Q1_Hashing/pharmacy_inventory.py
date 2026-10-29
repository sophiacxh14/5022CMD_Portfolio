"""
Question 1: Hashing - Pharmacy Inventory System
================================================
A command-line inventory system for a pharmacy.

* Products are stored in a hash table that resolves collisions using
  OPEN ADDRESSING with LINEAR PROBING.
* The same products are also stored in a one-dimensional array (a Python list),
  so the search speed of both data structures can be compared.

Run this file to start the program.
"""

import random
import time

# ---------------------------------------------------------------------------
# Settings (change them here, not inside the code)
# ---------------------------------------------------------------------------
DATA_SIZES = [100, 1000, 10000]    # number of records used in the experiment
SEARCHES_PER_TEST = 1000           # number of searches timed for each data size
MISSING_ID_START = 20000000        # IDs from here upwards are never stored


# ===========================================================================
# 1. ENTITY CLASS
# ===========================================================================
class Medicine:
    """One medicine product sold by the pharmacy."""

    def __init__(self, product_id, name, category, price, stock, needs_prescription=False):
        self.product_id = product_id                  # int   - unique key used for hashing
        self.name = name                              # str   - e.g. "Paracetamol 500mg"
        self.category = category                      # str   - e.g. "Pain Relief"
        self.price = price                            # float - price in RM
        self.stock = stock                            # int   - units in stock
        self.needs_prescription = needs_prescription  # bool  - True if a doctor's prescription is needed

    def __str__(self):
        """Text shown when a Medicine object is printed."""
        prescription = "Yes" if self.needs_prescription else "No"   # turn True/False into Yes/No
        return (f"ID: {self.product_id} | Name: {self.name} | Category: {self.category} | "
                f"Price: RM{self.price:.2f} | Stock: {self.stock} | Prescription: {prescription}")


# ===========================================================================
# 2. HASH TABLE (open addressing with linear probing)
#    It stores any key and value, so it can be reused for other kinds of data.
# ===========================================================================
class HashEntry:
    """What is stored in an occupied slot: a key and its value."""

    def __init__(self, key, value):
        self.key = key          # used to find the record, e.g. product ID 1042
        self.value = value      # the record itself, e.g. a Medicine object


class HashTable:
    """Hash table using open addressing with linear probing."""

    DELETED = "DELETED"  # marker ("tombstone") left in a slot when its entry is deleted

    def __init__(self, capacity=11, max_load_factor=0.7):
        self.capacity = capacity                 # total number of slots (11 is a prime number)
        self.max_load_factor = max_load_factor   # grow before the table is more than 70% full
        self.size = 0                            # number of entries stored
        # Each slot holds one of: None (empty), a HashEntry (occupied),
        # or DELETED (an entry used to be here)
        self.slots: list = [None] * capacity

    def hash_function(self, key):
        """Turn a key into a starting slot number from 0 to capacity - 1."""
        return hash(key) % self.capacity   # for whole numbers hash() returns the number itself, e.g. 1042 % 23 = 7

    def load_factor(self):
        """How full the table is (0.0 = empty, 1.0 = full)."""
        return self.size / self.capacity

    def insert(self, key, value):
        """Store a key and value. Returns the slot number used.
        If the key already exists, its value is replaced."""
        # Grow the table first if adding one more entry would make it too full
        if (self.size + 1) / self.capacity > self.max_load_factor:
            self.resize()

        index = self.hash_function(key)
        # If we pass a deleted slot, remember it in case the key is not found later.
        first_deleted = -1                 # first DELETED slot passed (-1 = none yet)

        for step in range(self.capacity):  # check each slot at most once (so the loop can never run forever)
            slot = self.slots[index]
            if slot is None:               # empty slot: the key is not in the table
                break
            if slot == self.DELETED:
                if first_deleted == -1:
                    first_deleted = index  # remember it so it can be reused
            elif slot.key == key:          # same key: update the existing record
                slot.value = value
                return index
            index = (index + 1) % self.capacity   # LINEAR PROBING: try the next slot
            # Modulo wraps the index back to 0 when it reaches the end of the table.

        if first_deleted != -1:            # reuse a DELETED slot if one was passed
            index = first_deleted
        self.slots[index] = HashEntry(key, value)
        self.size += 1
        return index

    def find_slot(self, key):
        """Follow the probing path. Returns the slot number of the key, or -1 if not found."""
        index = self.hash_function(key)
        for step in range(self.capacity):
            slot = self.slots[index]
            if slot is None:               # empty slot: the key cannot be further along
                return -1
            if slot != self.DELETED and slot.key == key:
                return index               # found
            index = (index + 1) % self.capacity   # DELETED or another key: keep probing
        return -1

    def search(self, key):
        """Return the value stored for this key, or None if it is not found."""
        index = self.find_slot(key)
        if index == -1:
            return None
        return self.slots[index].value

    def delete(self, key):
        """Remove a key. Returns the removed value, or None if it was not found."""
        index = self.find_slot(key)
        if index == -1:
            return None
        removed_value = self.slots[index].value
        self.slots[index] = self.DELETED        # leave a marker, NOT None, so probing still works
        # Keeping the marker prevents a search from stopping too early in a collision chain.
        self.size -= 1
        return removed_value

    def resize(self):
        """Move every entry into a bigger table (the next prime above double the size)."""
        old_slots = self.slots
        # Create a larger table; entries must be inserted again because their slot indexes change.
        self.capacity = next_prime(self.capacity * 2)
        self.slots = [None] * self.capacity
        self.size = 0
        for slot in old_slots:
            if slot is not None and slot != self.DELETED:
                self.insert(slot.key, slot.value)   # re-hash into the new table

    def get_all_keys(self):
        """Return a list of every key stored."""
        keys = []
        for slot in self.slots:
            if slot is not None and slot != self.DELETED:
                keys.append(slot.key)
        return keys

    def display_slots(self):
        """Print every slot so collisions and probing can be seen."""
        for index in range(self.capacity):
            slot = self.slots[index]
            if slot is None:
                content = "empty"
            elif slot == self.DELETED:
                content = "<deleted>"
            else:
                content = f"key {slot.key}"
            print(f"  [{index:>3}] {content}")      # >3 right-aligns the slot number in 3 spaces


def is_prime(number):
    """Return True if the number is prime."""
    if number < 2:
        return False
    for divisor in range(2, int(number ** 0.5) + 1):   # only need to test divisors up to the square root
        if number % divisor == 0:
            return False
    return True


def next_prime(number):
    """Return the smallest prime number that is equal to or bigger than the number."""
    while not is_prime(number):
        number += 1
    return number


# ===========================================================================
# 3. ONE-DIMENSIONAL ARRAY (for the performance comparison)
# ===========================================================================
def linear_search(array, product_id):
    """Check every medicine in the list, one by one, until the ID matches."""
    for medicine in array:
        if medicine.product_id == product_id:
            return medicine
    return None


# ===========================================================================
# 4. PRE-DEFINED RECORDS
# ===========================================================================
def load_sample_data(table, array):
    """Insert the same pre-defined medicines into the hash table AND the array."""
    medicines = [
        #        ID    Name                             Category          Price  Stock  Prescription
        Medicine(1042, "Paracetamol 500mg",             "Pain Relief",     5.90, 120),
        Medicine(1078, "Ibuprofen 200mg",               "Pain Relief",     8.50,  80),
        Medicine(1103, "Amoxicillin 500mg",             "Antibiotic",     18.00,  40, True),
        Medicine(1156, "Cetirizine 10mg",               "Allergy",        12.90,  60),
        Medicine(2011, "Loratadine 10mg",               "Allergy",        14.50,  55),
        Medicine(2047, "Omeprazole 20mg",               "Gastric",        22.00,  35, True),
        Medicine(2089, "Metformin 500mg",               "Diabetes",       15.00,  50, True),
        Medicine(3015, "Amlodipine 5mg",                "Blood Pressure", 19.90,  45, True),
        Medicine(3062, "Vitamin C 1000mg",              "Supplement",     25.90, 100),
        Medicine(3104, "Honey Lemon Throat Lozenges",   "Cough & Cold",    9.80, 150),
        Medicine(4026, "Dextromethorphan Syrup 100ml",  "Cough & Cold",   13.50,  30),
        Medicine(4073, "Oral Rehydration Salts",        "Digestive",       6.50,  70),
        Medicine(5019, "Salbutamol Inhaler 100mcg",     "Respiratory",    28.00,  20, True),
        Medicine(5058, "Chlorhexidine Mouthwash 250ml", "Oral Care",      16.90,  25),
        Medicine(6034, "Hydrocortisone Cream 1%",       "Skin Care",      11.20,  40),
    ]
    for medicine in medicines:
        # Store the same Medicine object in both structures for a fair comparison.
        table.insert(medicine.product_id, medicine)
        array.append(medicine)


# ===========================================================================
# 5. INPUT HELPERS (keep asking until the input is valid, so the program never crashes)
# ===========================================================================
def read_int(prompt, minimum=0):
    while True:
        text = input(prompt).strip()
        if text.isdigit() and int(text) >= minimum:   # isdigit() is False for letters, symbols and "-" signs
            return int(text)
        print(f"  Please enter a whole number of at least {minimum}.")


def read_float(prompt, minimum=0.0):
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
            if value >= minimum:
                return round(value, 2)     # keep 2 decimal places for Ringgit
        except ValueError:
            pass                           # not a number: show the message below
        print(f"  Please enter a number of at least {minimum:.2f}, e.g. 5.90")


def read_text(prompt):
    while True:
        text = input(prompt).strip()
        if text != "":
            return text
        print("  This field cannot be empty.")


def read_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()     # lower() lets "Y" and "y" both work
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please enter y or n.")


# ===========================================================================
# 6. MENU OPTIONS
# ===========================================================================
def insert_product(table, array):
    print("\n--- Insert Product ---")
    product_id = read_int("Enter Product ID: ", minimum=1)
    if table.search(product_id) is not None:       # reject duplicate IDs before asking for other details
        print(f"  Product ID {product_id} already exists. Use Edit to change it.")
        return

    name = read_text("Enter Product Name: ")
    category = read_text("Enter Category: ")
    price = read_float("Enter Price (RM): ")
    stock = read_int("Enter Stock Quantity: ")
    needs_prescription = read_yes_no("Requires prescription? (y/n): ")
    medicine = Medicine(product_id, name, category, price, stock, needs_prescription)

    old_capacity = table.capacity                  # remembered so we can tell the user if the table grew
    slot = table.insert(product_id, medicine)
    array.append(medicine)
    print(f"  Product inserted successfully into slot [{slot}].")
    if table.capacity != old_capacity:
        print(f"  (The table grew from {old_capacity} to {table.capacity} slots "
              f"to stay below {table.max_load_factor:.0%} full.)")


def search_product(table, array):
    print("\n--- Search Product ---")
    product_id = read_int("Enter Product ID to search: ", minimum=1)

    start = time.perf_counter_ns()                 # high-precision timer in nanoseconds
    medicine = table.search(product_id)
    table_time = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    linear_search(array, product_id)
    array_time = time.perf_counter_ns() - start

    if medicine is None:
        print(f"  Product ID {product_id} not found.")
    else:
        print("  Product found!")
        print(f"  {medicine}")
    print(f"  Search time (Hash Table): {table_time:>8,} ns")
    print(f"  Search time (Array)     : {array_time:>8,} ns")


def edit_product(table):
    print("\n--- Edit Product ---")
    product_id = read_int("Enter Product ID to edit: ", minimum=1)
    medicine = table.search(product_id)
    if medicine is None:
        print(f"  Product ID {product_id} not found.")
        return

    print(f"  Current: {medicine}")
    # The product ID cannot be edited: it is the hash key that decides which slot the product is in
    print("  1. Name  2. Category  3. Price  4. Stock  5. Prescription")
    field = input("  Which field do you want to change? ").strip()
    if field == "1":
        medicine.name = read_text("  New Name: ")
    elif field == "2":
        medicine.category = read_text("  New Category: ")
    elif field == "3":
        medicine.price = read_float("  New Price (RM): ")
    elif field == "4":
        medicine.stock = read_int("  New Stock Quantity: ")
    elif field == "5":
        medicine.needs_prescription = read_yes_no("  Requires prescription? (y/n): ")
    else:
        print("  Invalid field. Nothing was changed.")
        return
    # The hash table and the array hold the SAME Medicine object, so both are updated
    print(f"  Updated: {medicine}")


def delete_product(table, array):
    print("\n--- Delete Product ---")
    product_id = read_int("Enter Product ID to delete: ", minimum=1)
    medicine = table.search(product_id)
    if medicine is None:
        print(f"  Product ID {product_id} not found.")
        return

    print(f"  {medicine}")
    if read_yes_no("  Are you sure you want to delete this product? (y/n): "):
        table.delete(product_id)
        array.remove(medicine)             # remove it from the array too, so both hold the same data
        print(f"  '{medicine.name}' deleted successfully.")
    else:
        print("  Delete cancelled.")


def view_all_products(table):
    print(f"\n--- All Products ({table.size}) ---")
    print(f"  {'ID':<6}{'Name':<31}{'Category':<16}{'Price (RM)':>10}{'Stock':>7}  Rx")
    print("  " + "-" * 74)
    for product_id in sorted(table.get_all_keys()):      # sorted by ID for easy reading
        medicine = table.search(product_id)
        prescription = "Yes" if medicine.needs_prescription else "No"
        print(f"  {medicine.product_id:<6}{medicine.name:<31.30}{medicine.category:<16.15}"
              f"{medicine.price:>10.2f}{medicine.stock:>7}  {prescription}")


def view_slot_layout(table):
    print("\n--- Hash Table Slot Layout ---")
    print(f"  Items: {table.size} | Capacity: {table.capacity} | "
          f"Load factor: {table.load_factor():.2f}")
    table.display_slots()


# ===========================================================================
# 7. PERFORMANCE EXPERIMENT: hash table search vs array search
# ===========================================================================
def time_hash_table(table, search_ids):
    """Return the average time (ns) of one hash table search."""
    start = time.perf_counter_ns()
    for product_id in search_ids:
        table.search(product_id)
    return (time.perf_counter_ns() - start) / len(search_ids)


def time_array(array, search_ids):
    """Return the average time (ns) of one linear search in the array."""
    start = time.perf_counter_ns()
    for product_id in search_ids:
        linear_search(array, product_id)
    return (time.perf_counter_ns() - start) / len(search_ids)


def run_performance_experiment():
    random.seed(42)                        # same "random" data every time it runs
    print("\n=== Search Performance: Hash Table vs Array ===")
    print(f"Average time of ONE search, measured over {SEARCHES_PER_TEST:,} searches\n")
    print(f"{'Records':>8} | {'Search type':<12} | {'Hash Table':>12} | {'Array':>14} | {'Hash Table is'}")
    print("-" * 70)

    for size in DATA_SIZES:
        # Put the SAME records into both data structures
        table = HashTable()
        array = []
        product_ids = random.sample(range(1000, 10000000), size)   # unique random IDs
        for product_id in product_ids:
            medicine = Medicine(product_id, f"Test Medicine {product_id}", "Test", 10.00, 100)
            table.insert(product_id, medicine)
            array.append(medicine)

        # Search both structures for the SAME IDs so their timings can be compared fairly.
        found_ids = random.choices(product_ids, k=SEARCHES_PER_TEST)      # IDs that exist
        missing_ids = []
        for i in range(SEARCHES_PER_TEST):
            missing_ids.append(MISSING_ID_START + i)                      # IDs that do not exist

        # Measure successful and unsuccessful searches separately.
        for search_type, search_ids in [("Found", found_ids), ("Not found", missing_ids)]:
            table_ns = time_hash_table(table, search_ids)
            array_ns = time_array(array, search_ids)
            print(f"{size:>8,} | {search_type:<12} | {table_ns:>9,.0f} ns | "
                  f"{array_ns:>11,.0f} ns | {array_ns / table_ns:,.1f}x faster")   # array time / table time
        print("-" * 70)


# ===========================================================================
# 8. MAIN PROGRAM
# ===========================================================================
def main():
    table = HashTable()
    array = []
    load_sample_data(table, array)
    print(f"Loaded {table.size} pre-defined products.")

    while True:
        print("\n==== Pharmacy Inventory System ====")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. View All Products")
        print("6. View Hash Table Slot Layout")
        print("7. Run Performance Experiment")
        print("0. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            insert_product(table, array)
        elif choice == "2":
            search_product(table, array)
        elif choice == "3":
            edit_product(table)
        elif choice == "4":
            delete_product(table, array)
        elif choice == "5":
            view_all_products(table)
        elif choice == "6":
            view_slot_layout(table)
        elif choice == "7":
            run_performance_experiment()
        elif choice == "0":
            print("Exiting Pharmacy Inventory System. Goodbye!")
            break
        else:
            print("  Invalid choice. Please enter a number from the menu.")


# Run the menu only when this file is executed directly, not when it is imported.
if __name__ == "__main__":
    main()