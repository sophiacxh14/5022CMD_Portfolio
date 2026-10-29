"""
inventory_system.py
-------------------
Command-line Pharmacy Inventory System (run this file to start the program).

Every product is stored in BOTH the hash table (the main storage) and a plain
array, so each search can show how long each data structure took.
"""

import time
from typing import Any

from array_storage import ArrayStorage
from hash_table import HashTable
from medicine import Medicine
from sample_data import get_sample_medicines


# ---------------------------------------------------------------------------
# Input helpers: keep asking until the user types something valid
# ---------------------------------------------------------------------------
def read_int(prompt: str, minimum: int = 0) -> int:
    """Ask for a whole number that is at least `minimum`."""
    while True:
        text = input(prompt).strip()
        try:
            value = int(text)
        except ValueError:
            print("  Please enter a whole number.")
        else:
            if value >= minimum:
                return value
            print(f"  Please enter a number of at least {minimum}.")


def read_float(prompt: str, minimum: float = 0.0) -> float:
    """Ask for a decimal number that is at least `minimum`."""
    while True:
        text = input(prompt).strip()
        try:
            value = float(text)
        except ValueError:
            print("  Please enter a number, e.g. 5.90")
        else:
            if value >= minimum:
                return value
            print(f"  Please enter a value of at least {minimum}.")


def read_text(prompt: str) -> str:
    """Ask for text that is not empty."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("  This field cannot be empty.")


def read_yes_no(prompt: str) -> bool:
    """Ask a yes/no question and return True for yes, False for no."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please enter y or n.")


def timed_search(storage: Any, key: Any) -> tuple[Any, int]:
    """
    Search any storage that has a .search() method (HashTable or ArrayStorage)
    and return (result, time taken in nanoseconds).
    """
    start = time.perf_counter_ns()
    result = storage.search(key)
    elapsed = time.perf_counter_ns() - start
    return result, elapsed


# ---------------------------------------------------------------------------
# The inventory system
# ---------------------------------------------------------------------------
class PharmacyInventorySystem:
    """Menu-driven pharmacy inventory backed by a hash table."""

    def __init__(self) -> None:
        self.table = HashTable()       # main storage
        self.array = ArrayStorage()    # same data, used for speed comparison
        self._load_sample_data()

    def _load_sample_data(self) -> None:
        """Insert the pre-defined records into BOTH data structures."""
        for medicine in get_sample_medicines():
            self.table.insert(medicine.product_id, medicine)
            self.array.insert(medicine.product_id, medicine)

    # ---------------------------- menu actions ----------------------------
    def insert_product(self) -> None:
        print("\n--- Insert New Product ---")
        product_id = read_int("Enter Product ID: ", minimum=1)
        if product_id in self.table:
            print(f"  Product ID {product_id} already exists. Use Edit to change it.")
            return

        name = read_text("Enter Product Name: ")
        category = read_text("Enter Category: ")
        price = read_float("Enter Price (RM): ")
        stock = read_int("Enter Stock Quantity: ")
        prescription = read_yes_no("Requires prescription? (y/n): ")

        medicine = Medicine(product_id, name, category, price, stock, prescription)
        old_capacity = self.table.capacity
        slot = self.table.insert(product_id, medicine)
        self.array.insert(product_id, medicine)

        print(f"  Product inserted successfully into slot [{slot}].")
        if self.table.capacity != old_capacity:
            print(f"  (Table grew from {old_capacity} to {self.table.capacity} slots "
                  f"to keep the load factor below {HashTable.MAX_LOAD_FACTOR:.0%}.)")

    def search_product(self) -> None:
        print("\n--- Search Product ---")
        product_id = read_int("Enter Product ID to search: ", minimum=1)

        medicine, table_time = timed_search(self.table, product_id)
        _, array_time = timed_search(self.array, product_id)

        if medicine is None:
            print(f"  Product ID {product_id} not found.")
        else:
            print("  Product found!")
            print(f"  {medicine}")
        print(f"  Search time (Hash Table): {table_time:>8,} ns")
        print(f"  Search time (Array)     : {array_time:>8,} ns")

    def edit_product(self) -> None:
        print("\n--- Edit Product ---")
        product_id = read_int("Enter Product ID to edit: ", minimum=1)
        medicine = self.table.search(product_id)
        if medicine is None:
            print(f"  Product ID {product_id} not found.")
            return

        print(f"  Current: {medicine}")
        print("  Which field do you want to change?")
        print("  1. Name   2. Category   3. Price   4. Stock   5. Prescription")
        field = input("  Enter field number: ").strip()

        if field == "1":
            medicine.name = read_text("  New Name: ")
        elif field == "2":
            medicine.category = read_text("  New Category: ")
        elif field == "3":
            medicine.price = round(read_float("  New Price (RM): "), 2)
        elif field == "4":
            medicine.stock_quantity = read_int("  New Stock Quantity: ")
        elif field == "5":
            medicine.requires_prescription = read_yes_no("  Requires prescription? (y/n): ")
        else:
            print("  Invalid field. Nothing was changed.")
            return

        # Both structures hold the SAME Medicine object, so one change updates both
        print("  Product updated successfully!")
        print(f"  Updated: {medicine}")

    def delete_product(self) -> None:
        print("\n--- Delete Product ---")
        product_id = read_int("Enter Product ID to delete: ", minimum=1)
        medicine = self.table.search(product_id)
        if medicine is None:
            print(f"  Product ID {product_id} not found.")
            return

        print(f"  {medicine}")
        if not read_yes_no("  Are you sure you want to delete this product? (y/n): "):
            print("  Delete cancelled.")
            return

        self.table.delete(product_id)     # leaves a tombstone in its slot
        self.array.delete(product_id)     # later items shift left
        print(f"  '{medicine.name}' deleted successfully.")

    def view_all_products(self) -> None:
        print(f"\n--- All Products ({len(self.table)}) ---")
        if len(self.table) == 0:
            print("  The inventory is empty.")
            return

        header = (f"  {'ID':<6}{'Name':<31}{'Category':<16}"
                  f"{'Price (RM)':>11}{'Stock':>7}  {'Rx':<3}")
        print(header)
        print("  " + "-" * (len(header) - 2))

        # Hash tables are unordered, so sort by product ID for a readable list
        for product_id, medicine in sorted(self.table.items()):
            rx = "Yes" if medicine.requires_prescription else "No"
            print(f"  {product_id:<6}{medicine.name:<31.30}{medicine.category:<16.15}"
                  f"{medicine.price:>11.2f}{medicine.stock_quantity:>7}  {rx:<3}")

    def view_slot_layout(self) -> None:
        print("\n--- Hash Table Slot Layout ---")
        print(f"  Items: {len(self.table)} | Capacity: {self.table.capacity} | "
              f"Load factor: {self.table.load_factor:.2f}")
        print(self.table)

    # ------------------------------ main loop ------------------------------
    @staticmethod
    def _show_menu() -> None:
        print("\n==== Pharmacy Inventory System ====")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Edit Product")
        print("4. Delete Product")
        print("5. View All Products")
        print("6. View Hash Table Slot Layout")
        print("0. Exit")

    def run(self) -> None:
        print(f"Loaded {len(self.table)} pre-defined products.")
        while True:
            self._show_menu()
            choice = input("Enter choice: ").strip()

            if choice == "1":
                self.insert_product()
            elif choice == "2":
                self.search_product()
            elif choice == "3":
                self.edit_product()
            elif choice == "4":
                self.delete_product()
            elif choice == "5":
                self.view_all_products()
            elif choice == "6":
                self.view_slot_layout()
            elif choice == "0":
                print("Exiting Pharmacy Inventory System. Goodbye!")
                break
            else:
                print("  Invalid choice. Please enter a number from the menu.")


if __name__ == "__main__":
    PharmacyInventorySystem().run()