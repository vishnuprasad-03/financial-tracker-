import json

from src.io_manager import import_csv, export_json
from src.models import Category, Transaction


def test_export_json_creates_file(tmp_path):
    transactions = [
        Transaction(100, Category("Food"), "expense")
    ]

    file = tmp_path / "transactions.json"

    export_json(transactions, file)

    assert file.exists()


def test_export_json_content(tmp_path):
    transactions = [
        Transaction(250, Category("Food"), "expense")
    ]

    file = tmp_path / "transactions.json"

    export_json(transactions, file)

    with open(file, "r") as f:
        data = json.load(f)

    assert data[0]["amount"] == 250
    assert data[0]["category"] == "Food"
    assert data[0]["transaction_type"] == "expense"


def test_import_csv_single(tmp_path):
    file = tmp_path / "sample.csv"

    file.write_text(
        "amount,category,transaction_type\n"
        "100,Food,expense\n"
    )

    transactions = import_csv(file)

    assert len(transactions) == 1
    assert transactions[0].amount == 100


def test_import_csv_multiple(tmp_path):
    file = tmp_path / "sample.csv"

    file.write_text(
        "amount,category,transaction_type\n"
        "100,Food,expense\n"
        "500,Salary,income\n"
    )

    transactions = import_csv(file)

    assert len(transactions) == 2


def test_import_csv_invalid_row(tmp_path):
    file = tmp_path / "sample.csv"

    file.write_text(
        "amount,category,transaction_type\n"
        "-100,Food,expense\n"
    )

    transactions = import_csv(file)

    assert len(transactions) == 0