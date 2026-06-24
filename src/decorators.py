"""
Custom decorators for Finance Tracker.
"""

import time


def timer(func):
    """
    Measure execution time.
    """

    def wrapper(*args, **kwargs):

        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        print(
            f"Execution Time: "
            f"{end-start:.6f} sec"
        )

        return result

    return wrapper


def validate_amount(func):
    """
    Validate amount before execution.
    """

    def wrapper(self, amount, *args, **kwargs):

        if amount <= 0:
            raise ValueError(
                "Amount must be greater than 0"
            )

        return func(
            self,
            amount,
            *args,
            **kwargs
        )

    return wrapper
