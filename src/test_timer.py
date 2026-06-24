from src.decorators import timer
from src.models import (
    Category,
    Transaction
)


@timer
def create_transactions():

    food = Category("Food")

    for _ in range(10000):

        Transaction(
            100,
            food,
            "expense"
        )


create_transactions()
