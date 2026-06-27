"""
Domain models for Finance Tracker.

Contains:
- Transaction
- Category
"""

from src.decorators import validate_amount

from src.exceptions import (
    InvalidAmountError,
    InvalidCategoryError,
    InvalidTransactionTypeError
)

class Category:
    """
    Represents a transaction category.

    Example:
        Food
        Travel
        Salary
    """

    def __init__(self, name: str):
        """
        Initialize category.

        Args:
            name (str): Category name.
        """

        if not isinstance(name, str):
            raise TypeError(
                "Category name must be a string."
            )

        if not name.strip():
           raise InvalidCategoryError(
    "Category name cannot be empty."
   )

        self.name = name.strip()

    def __str__(self):
        """
        Return readable string.
        """
        return self.name


class Transaction:
    """
    Represents a financial transaction.
    """

    __slots__ = (
        "amount",
        "category",
        "transaction_type"
    )

    VALID_TYPES = (
        "income",
        "expense"
    )

    def __init__(
        self,
        amount: float,
        category: Category,
        transaction_type: str
    ):
        """
        Initialize transaction.

        Args:
            amount (float):
                Transaction amount.

            category (Category):
                Transaction category.

            transaction_type (str):
                income or expense.
        """

        if amount <= 0:
            raise InvalidAmountError(
                "Amount must be greater than zero."
    )

        if not isinstance(
            category,
            Category
        ):
            raise InvalidCategoryError(
                "category must be Category object."
            )

        if (
            transaction_type
            not in self.VALID_TYPES
        ):
            raise InvalidTransactionTypeError(
    "Transaction type must be 'income' or 'expense'."
)

        self.amount = amount
        self.category = category
        self.transaction_type = transaction_type

    def __str__(self):
        """
        Human-readable display.
        """

        return (
            f"{self.transaction_type.upper()} | "
            f"₹{self.amount:.2f} | "
            f"{self.category}"
        )

    def __eq__(self, other):
        """
        Equality comparison.
        """

        return (
            self.amount == other.amount
            and
            self.category.name
            ==
            other.category.name
            and
            self.transaction_type
            ==
            other.transaction_type
        )

    def __lt__(self, other):
        """
        Less-than comparison.
        """

        return (
            self.amount
            <
            other.amount
        )
    @validate_amount
    def update_amount(
        self,
        amount: float
    ):
        """
        Update transaction amount.
        """

        self.amount = amount
