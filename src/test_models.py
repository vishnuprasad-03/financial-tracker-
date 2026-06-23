from src.models import (
    Category,
    Transaction
)

food = Category("Food")

expense = Transaction(
    300,
    food,
    "expense"
)

assert food.name == "Food"

assert expense.amount == 300

assert expense.transaction_type == "expense"

assert str(food) == "Food"

print("All tests passed!")

