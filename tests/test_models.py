import pytest

from src.models import Category, Transaction
from src.exceptions import (
    InvalidAmountError,
    InvalidCategoryError,
    InvalidTransactionTypeError,
)


# ---------- Category Tests ----------

def test_category_creation():
    c = Category("Food")
    assert c.name == "Food"


def test_category_strip_spaces():
    c = Category("  Travel  ")
    assert c.name == "Travel"


def test_category_empty():
    with pytest.raises(InvalidCategoryError):
        Category("")


def test_category_not_string():
    with pytest.raises(TypeError):
        Category(123)


def test_category_str():
    c = Category("Salary")
    assert str(c) == "Salary"


# ---------- Transaction Tests ----------

def test_transaction_creation():
    c = Category("Food")
    t = Transaction(200, c, "expense")

    assert t.amount == 200
    assert t.category == c
    assert t.transaction_type == "expense"


def test_transaction_invalid_amount():
    c = Category("Food")

    with pytest.raises(InvalidAmountError):
        Transaction(0, c, "expense")


def test_transaction_invalid_category():
    with pytest.raises(InvalidCategoryError):
        Transaction(100, "Food", "expense")


def test_transaction_invalid_type():
    c = Category("Food")

    with pytest.raises(InvalidTransactionTypeError):
        Transaction(100, c, "shopping")


def test_transaction_str():
    c = Category("Food")
    t = Transaction(250, c, "expense")

    assert str(t) == "EXPENSE | ₹250.00 | Food"


def test_transaction_equal():
    c = Category("Food")

    t1 = Transaction(200, c, "expense")
    t2 = Transaction(200, c, "expense")

    assert t1 == t2


def test_transaction_less_than():
    c = Category("Food")

    t1 = Transaction(100, c, "expense")
    t2 = Transaction(300, c, "expense")

    assert t1 < t2


def test_update_amount():
    c = Category("Food")
    t = Transaction(100, c, "expense")

    t.update_amount(500)

    assert t.amount == 500


def test_update_amount_invalid():
    c = Category("Food")
    t = Transaction(100, c, "expense")

    with pytest.raises(ValueError):
        t.update_amount(-50)