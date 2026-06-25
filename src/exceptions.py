"""
Custom exceptions for the Finance Tracker.
"""


class TransactionError(Exception):
    """
    Base exception for all transaction-related errors.
    """
    pass


class InvalidAmountError(TransactionError):
    """
    Raised when the transaction amount is invalid.
    """
    pass


class InvalidCategoryError(TransactionError):
    """
    Raised when the transaction category is invalid.
    """
    pass


class InvalidTransactionTypeError(TransactionError):
    """
    Raised when the transaction type is invalid.
    """
    pass