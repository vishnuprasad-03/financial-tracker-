"""
Transaction routes.
"""

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import login_required

from src.database import SessionLocal
from src.db_models import TransactionDB
from src.forms import TransactionForm
from src.exchange_service import get_usd_rate

transactions_bp = Blueprint(
    "transactions",
    __name__
)




@transactions_bp.route(
    "/transactions",
    methods=["GET", "POST"]
)
@login_required
def transactions():

    form = TransactionForm()

    session = SessionLocal()

    if form.validate_on_submit():

        transaction = TransactionDB(

            amount=form.amount.data,

            category=form.category.data,

            transaction_type=form.transaction_type.data

        )

        session.add(transaction)

        session.commit()

        flash(
            "Transaction added successfully!",
            "success"
        )

        session.close()

        return redirect(
            url_for("transactions.transactions")
        )

    all_transactions = session.query(
        TransactionDB
    ).all()

    total_income = sum(
        transaction.amount
        for transaction in all_transactions
        if transaction.transaction_type == "income"
    )

    total_expense = sum(
        transaction.amount
        for transaction in all_transactions
        if transaction.transaction_type == "expense"
    )

    balance = total_income - total_expense
    usd_rate = get_usd_rate()
    total_spend_usd = total_expense * usd_rate

    session.close()

    return render_template(
    "transactions.html",
    form=form,
    transactions=all_transactions,
    total_income=total_income,
    total_expense=total_expense,
    balance=balance,
    usd_rate=usd_rate,
    total_spend_usd=total_spend_usd

)