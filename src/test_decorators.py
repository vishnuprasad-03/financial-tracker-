from src.models import Category, Transaction

food = Category("Food")

t = Transaction(
    100,
    food,
    "expense"
)

t.update_amount(500)

print(t)
