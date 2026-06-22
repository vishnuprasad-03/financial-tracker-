import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "--income",
    type=float,
    help="Add income"
)

args = parser.parse_args()

if args.income:
    print(
        f"Income Added: ₹{args.income}"
    )
