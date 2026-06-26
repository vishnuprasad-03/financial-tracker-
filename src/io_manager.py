"""
Input/Output manager for Finance Tracker.
"""

import csv
import json
from pathlib import Path

from src.models import Transaction, Category
from src.logger_config import logger


def import_csv(file_path: str):
    """
    Import transactions from a CSV file.
    """

    transactions = []

    path = Path(file_path)

    with path.open(
        mode="r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            try:

                category = Category(
                    row["category"]
                )

                transaction = Transaction(
                    float(row["amount"]),
                    category,
                    row["transaction_type"]
                )

                transactions.append(transaction)

            except Exception as error:

                logger.error(
                    f"Malformed row skipped: {row} | {error}"
                )

    return transactions

def export_json(
    transactions,
    file_path: str
):
    """
    Export transactions to a JSON file.
    """

    data = []

    for transaction in transactions:

        data.append({

            "amount":
                transaction.amount,

            "category":
                transaction.category.name,

            "transaction_type":
                transaction.transaction_type

        })

    path = Path(file_path)

    with path.open(
        mode="w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )