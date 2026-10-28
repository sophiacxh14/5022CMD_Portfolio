"""
array_storage.py
----------------
A simple one-dimensional array (Python list) that stores key -> value pairs
and finds them with LINEAR SEARCH. It offers the same methods as HashTable
(insert, search, delete), so both can be tested with the same data in a fair
performance comparison.
"""

from typing import Any


class ArrayStorage:
    """Stores key/value pairs in a plain list and searches them one by one."""

    def __init__(self) -> None:
        self._items: list[tuple[Any, Any]] = []    # each item is a (key, value) pair

    def __len__(self) -> int:
        """Number of entries stored, so len(array) works."""
        return len(self._items)

    def _find_position(self, key: Any) -> int | None:
        """
        LINEAR SEARCH: check every item from the start until the key matches.
        Return its position, or None if the key is not stored.
        """
        for position, (stored_key, _) in enumerate(self._items):
            if stored_key == key:
                return position
        return None

    def insert(self, key: Any, value: Any) -> int:
        """Add a key/value pair (or update it if the key exists) and return its position."""
        position = self._find_position(key)
        if position is not None:
            self._items[position] = (key, value)    # same key: update, no duplicates
            return position

        self._items.append((key, value))            # new key: add to the end
        return len(self._items) - 1

    def search(self, key: Any) -> Any:
        """Return the value stored with this key, or None if the key is not found."""
        position = self._find_position(key)
        if position is None:
            return None
        return self._items[position][1]             # [1] = the value part of the pair

    def delete(self, key: Any) -> Any:
        """Remove the entry with this key and return its value, or None if not found."""
        position = self._find_position(key)
        if position is None:
            return None
        _, removed_value = self._items.pop(position)   # later items shift left by one
        return removed_value


# ---------------------------------------------------------------------------
# Quick test: only runs when this file is run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from sample_data import get_sample_medicines

    array = ArrayStorage()
    for medicine in get_sample_medicines():
        array.insert(medicine.product_id, medicine)

    print("Items stored:", len(array))
    print("Search 1042 (first item):", array.search(1042))
    print("Search 6034 (last item): ", array.search(6034))
    print("Search 9999 (missing):   ", array.search(9999))
    print("Delete 1042:", array.delete(1042))
    print("Items after delete:", len(array))