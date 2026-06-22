import argparse

parser = argparse.ArgumentParser(
    description="Finance Tracker CLI"
)

parser.add_argument(
    "--income",
    type=float,
    help="Add income amount"
)

parser.add_argument(
    "--expense",
    type=float,
    help="Add expense amount"
)

parser.add_argument(
    "--category",
    type=str,
    help="Expense category"
)

args = parser.parse_args()

if args.income:
    print(f"Income Added: ₹{args.income}")

if args.expense:
    print(f"Expense Added: ₹{args.expense}")

if args.category:
    print(f"Category: {args.category}")
