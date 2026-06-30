"""
Test budget module.
"""

from src.budget import check_budget
from src.exceptions import BudgetExceededError

try:
    check_budget()
    print("All categories are within budget.")

except BudgetExceededError as error:
    print(f"\033[91m{error}\033[0m")