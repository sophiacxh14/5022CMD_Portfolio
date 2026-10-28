"""
sample_data.py
--------------
Pre-defined pharmacy records loaded when the system starts.
Kept in one place so the inventory system AND the performance
experiment use exactly the same data.
"""

from medicine import Medicine


def get_sample_medicines() -> list[Medicine]:
    """Return a fresh list of pre-defined Medicine objects."""
    return [
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


# ---------------------------------------------------------------------------
# Quick test: load every sample medicine into the hash table
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from hash_table import HashTable

    table = HashTable()
    for medicine in get_sample_medicines():
        table.insert(medicine.product_id, medicine)

    print(f"Loaded {len(table)} medicines | Capacity: {table.capacity} | "
          f"Load factor: {table.load_factor:.2f}\n")

    print("Home slot of each medicine (product ID % capacity):")
    for medicine in get_sample_medicines():
        print(f"  {medicine.product_id} -> home slot {medicine.product_id % table.capacity}")

    print("\nActual slot layout:")
    print(table)

    print("\nSearch 4026 ->", table.search(4026))