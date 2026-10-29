"""
hash_table.py
-------------
A generic hash table that uses OPEN ADDRESSING with LINEAR PROBING
to resolve collisions. It stores key -> value pairs and knows nothing
about medicines, so it can be reused for any kind of data.
"""

from typing import Any, Iterator


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
        if first_tombstone is None:
            # Safety check: resizing keeps the table below 70% full,
            # so this should never happen
            raise RuntimeError("Hash table is unexpectedly full.")
        self._slots[first_tombstone] = HashEntry(key, value)
        self._size += 1
        return first_tombstone

    # ------------------------------------------------------------------
    # SEARCH AND DELETE
    # ------------------------------------------------------------------
    def _find_index(self, key: Any) -> int | None:
        """
        Follow the probing path for this key.
        Return the slot index holding the key, or None if the key is not stored.
        Shared by search() and delete() so the probing logic is written once.
        """
        index = self._hash(key)  # start at the key's home slot

        for _ in range(self._capacity):
            slot = self._slots[index]

            if slot is None:
                return None  # empty slot: key does not exist
            if slot is not self._DELETED and slot.key == key:
                return index  # found it

            index = (index + 1) % self._capacity  # tombstone or other key: keep probing

        return None  # every slot checked: not found

    def search(self, key: Any) -> Any:
        """Return the value stored with this key, or None if the key is not found."""
        index = self._find_index(key)
        if index is None:
            return None
        return self._slots[index].value

    def __contains__(self, key: Any) -> bool:
        """Allow 'key in table' to check whether a key exists."""
        return self._find_index(key) is not None

    def delete(self, key: Any) -> Any:
        """Remove the entry with this key and return its value, or None if not found."""
        index = self._find_index(key)
        if index is None:
            return None

        removed_value = self._slots[index].value
        self._slots[index] = self._DELETED  # leave a tombstone, NOT None
        self._size -= 1
        return removed_value

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
    def items(self) -> Iterator[tuple[Any, Any]]:
        """Give back every stored (key, value) pair, one at a time, in slot order."""
        for slot in self._slots:
            if isinstance(slot, HashEntry):  # skip empty slots and tombstones
                yield slot.key, slot.value

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
    table.insert(1042, "Paracetamol 500mg")  # home slot 8
    table.insert(2032, "Ibuprofen 200mg")  # also wants slot 8, probed to slot 9

    print("Deleted:", table.delete(1042))  # slot 8 becomes a tombstone
    print(table)
    print("Search 2032 after deleting 1042:", table.search(2032))  # must still be found
    print("Delete 1042 again:", table.delete(1042))  # already gone
    print("Re-inserted 1042 into slot", table.insert(1042, "Paracetamol 500mg"))  # reuses tombstone
    print("Items stored:", len(table))