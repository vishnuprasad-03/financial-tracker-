from src.io_manager import (
    import_csv,
    export_json
)

transactions = import_csv(
    "data/transactions.csv"
)

print("Imported Transactions:\n")

for transaction in transactions:
    print(transaction)

print(
    f"\nTotal Valid Transactions: {len(transactions)}"
)

export_json(
    transactions,
    "data/output.json"
)

print(
    "\nTransactions exported successfully!"
)