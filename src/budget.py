"""
Budget management for Finance Tracker.
"""

from src.exceptions import BudgetExceededError
from src.reports import category_summary


def check_budget():
    """
    Check whether any category exceeds
    its monthly budget.
    """
    budgets = {
    "Food": 500,
    "Travel": 400,
    "Shopping": 300,
    "Entertainment": 250,
    "Bills": 1000
}
    summary = category_summary()

    for category, spent in summary:

        budget_limit = budgets.get(category)

        if budget_limit is None:
            continue

        if spent > budget_limit:
            raise BudgetExceededError(
                f"{category} exceeded its monthly budget! "
                f"(Spent: ₹{spent:.2f}, Budget: ₹{budget_limit:.2f})"
            )