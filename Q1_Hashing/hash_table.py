"""
hash_table.py
-------------
A generic hash table that uses OPEN ADDRESSING with LINEAR PROBING
to resolve collisions. It stores key -> value pairs and knows nothing
about medicines, so it can be reused for any kind of data.
"""

from typing import Any


class HashEntry:
    """One occupied slot in the hash table: a key and the value stored with it."""

    def __init__(self, key: Any, value: Any) -> None:
        self.key = key        # used to find the record (e.g. product ID 1042)
        self.value = value    # the record itself (e.g. a Medicine object)


class HashTable:
    """Hash table using open addressing with linear probing."""

    # Special marker left in a slot after its entry is deleted (a "tombstone")
    _DELETED = object()

    # When the table becomes more than 70% full, it will grow automatically
    MAX_LOAD_FACTOR = 0.7

    def __init__(self, capacity: int = 11) -> None:
        if capacity < 1:
            raise ValueError("Capacity must be at least 1.")
        self._capacity = capacity

        # The slots: a fixed-size list. Every slot is always ONE of these:
        #   None       -> empty, never used
        #   HashEntry  -> occupied by a key/value pair
        #   _DELETED   -> held an entry that was later deleted (tombstone)
        self._slots: list = [None] * capacity

        self._size = 0    # number of entries currently stored

    def _hash(self, key: Any) -> int:
        """Convert a key into a starting slot index from 0 to capacity - 1."""
        return hash(key) % self._capacity

    def __len__(self) -> int:
        """Number of entries stored, so len(table) works."""
        return self._size

    @property
    def capacity(self) -> int:
        """Total number of slots in the table."""
        return self._capacity

    @property
    def load_factor(self) -> float:
        """How full the table is, from 0.0 (empty) to 1.0 (full)."""
        return self._size / self._capacity

    # ------------------------------------------------------------------
    # INSERT
    # ------------------------------------------------------------------
    def insert(self, key: Any, value: Any) -> int:
        """
        Store a key/value pair and return the slot index it was placed in.
        If the key already exists, its value is updated (no duplicate keys).
        """
        # Grow the table first if one more entry would make it too full
        if (self._size + 1) / self._capacity > self.MAX_LOAD_FACTOR:
            self._resize()

        index = self._hash(key)     # starting slot from the hash function
        first_tombstone = None      # first deleted slot passed (can be reused)

        # Linear probing: visit at most every slot once
        for _ in range(self._capacity):
            slot = self._slots[index]

            if slot is None:
                # Empty slot reached, so the key is not in the table.
                # Reuse an earlier tombstone if we passed one, otherwise use this slot.
                if first_tombstone is not None:
                    index = first_tombstone
                self._slots[index] = HashEntry(key, value)
                self._size += 1
                return index

            if slot is self._DELETED:
                if first_tombstone is None:
                    first_tombstone = index          # remember it, keep probing
            elif slot.key == key:
                slot.value = value                   # same key: update the record
                return index

            index = (index + 1) % self._capacity     # probe the next slot (wrap round)

        # Every slot was visited without finding an empty one,
        # so the new entry goes into the first tombstone found
        self._slots[first_tombstone] = HashEntry(key, value)
        self._size += 1
        return first_tombstone

    # ------------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------------
    def search(self, key: Any) -> Any:
        """Return the value stored with this key, or None if the key is not found."""
        index = self._hash(key)                      # start at the key's home slot

        for _ in range(self._capacity):
            slot = self._slots[index]

            if slot is None:
                return None                          # empty slot: key does not exist
            if slot is not self._DELETED and slot.key == key:
                return slot.value                    # found it

            index = (index + 1) % self._capacity     # tombstone or other key: keep probing

        return None                                  # every slot checked: not found

    def __contains__(self, key: Any) -> bool:
        """Allow 'key in table' to check whether a key exists."""
        return self.search(key) is not None

    # ------------------------------------------------------------------
    # RESIZING (private helpers)
    # ------------------------------------------------------------------
    def _resize(self) -> None:
        """Grow to a larger prime capacity and re-insert every entry (rehashing)."""
        old_slots = self._slots
        self._capacity = self._next_prime(self._capacity * 2)
        self._slots = [None] * self._capacity
        self._size = 0

        for slot in old_slots:
            if isinstance(slot, HashEntry):          # skip empty slots and tombstones
                self.insert(slot.key, slot.value)

    @staticmethod
    def _is_prime(number: int) -> bool:
        """Return True if number is prime."""
        if number < 2:
            return False
        divisor = 2
        while divisor * divisor <= number:
            if number % divisor == 0:
                return False
            divisor += 1
        return True

    @staticmethod
    def _next_prime(number: int) -> int:
        """Return the smallest prime number that is >= number."""
        while not HashTable._is_prime(number):
            number += 1
        return number

    # ------------------------------------------------------------------
    # DISPLAY
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        """Show the contents of every slot, so the effect of probing is visible."""
        lines = []
        for index, slot in enumerate(self._slots):
            if slot is None:
                content = "empty"
            elif slot is self._DELETED:
                content = "<deleted>"
            else:
                content = f"key {slot.key}"
            lines.append(f"[{index:>3}] {content}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Quick test: only runs when this file is run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    table = HashTable()
    table.insert(1042, "Paracetamol 500mg")   # home slot 8
    table.insert(2032, "Ibuprofen 200mg")     # also wants slot 8, probed to slot 9

    print("Search 1042:", table.search(1042))   # found in its home slot
    print("Search 2032:", table.search(2032))   # found after probing 1 step
    print("Search 1053:", table.search(1053))   # wants slot 8 too, but does not exist
    print("Is 2032 in the table?", 2032 in table)
    print("Is 1053 in the table?", 1053 in table)