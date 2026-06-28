"""
Migrate CSV data to SQLite.
"""

from src.io_manager import import_csv
from src.database import SessionLocal
from src.db_models import TransactionDB


def migrate():
    db = SessionLocal()

    transactions = import_csv("data/transactions.csv")

    for transaction in transactions:

        db_transaction = TransactionDB(
            amount=transaction.amount,
            category=transaction.category.name,
            transaction_type=transaction.transaction_type
        )

        db.add(db_transaction)

    db.commit()

    row_count = db.query(TransactionDB).count()

    print(f"CSV Transactions : {len(transactions)}")
    print(f"Database Rows    : {row_count}")

    if len(transactions) == row_count:
        print("✅ Migration Successful!")
    else:
        print("❌ Row count mismatch!")

    db.close()


if __name__ == "__main__":
    migrate()