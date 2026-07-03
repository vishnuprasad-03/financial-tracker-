"""
Transaction routes.
"""

from flask import Blueprint, render_template

from src.database import SessionLocal
from src.db_models import TransactionDB
from flask_login import login_required

transactions_bp = Blueprint(
    "transactions",
    __name__
)


@transactions_bp.route("/transactions")
@login_required
def transactions():

    session = SessionLocal()

    all_transactions = session.query(
        TransactionDB
    ).all()

    session.close()

    return render_template(
        "transactions.html",
        transactions=all_transactions
    )