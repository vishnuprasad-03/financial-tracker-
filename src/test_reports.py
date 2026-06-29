"""
Test reports module.
"""

from src.reports import category_summary


summary = category_summary()

print("Top 3 Spending Categories:\n")

for category, total in summary:
    print(f"{category}: ₹{total:.2f}")