"""
medicine.py
-----------
Entity class representing a single medicine product sold by the pharmacy.
Objects of this class are the records stored inside the hash table.
"""


class Medicine:
    """Represents one medicine product in the pharmacy inventory."""

    def __init__(self, product_id: int, name: str, category: str,
                 price: float, stock_quantity: int,
                 requires_prescription: bool = False) -> None:
        # Validate the data first, so the inventory can never hold an invalid record
        if product_id <= 0:
            raise ValueError("Product ID must be a positive whole number.")
        if not name.strip():
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")

        # Store the data inside this object (these are the "attributes")
        self.product_id = product_id                     # unique key used for hashing
        self.name = name.strip()                         # e.g. "Paracetamol 500mg"
        self.category = category.strip()                 # e.g. "Pain Relief"
        self.price = round(price, 2)                     # Ringgit, 2 decimal places
        self.stock_quantity = stock_quantity             # units currently in stock
        self.requires_prescription = requires_prescription  # True = needs doctor's note

    def __str__(self) -> str:
        """Return a neat one-line description, used whenever the object is printed."""
        prescription = "Yes" if self.requires_prescription else "No"
        return (f"ID: {self.product_id} | Name: {self.name} | "
                f"Category: {self.category} | Price: RM{self.price:.2f} | "
                f"Stock: {self.stock_quantity} | Prescription: {prescription}")


# ---------------------------------------------------------------------------
# Quick test: this part only runs when you run THIS file directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    paracetamol = Medicine(1042, "Paracetamol 500mg", "Pain Relief", 5.90, 120)
    print(paracetamol)

    # Try to create an invalid medicine, to prove the validation works
    try:
        Medicine(1043, "Bad Product", "Test", -3.00, 10)
    except ValueError as error:
        print("Validation caught an error:", error)