"""
Transaction routes.
"""

from flask import (
    Blueprint,
    render_template,
    redirect,
    session,
    url_for,
    flash,
    request
)

from flask_login import login_required
from flask_wtf import form
from datetime import date
from dateutil.relativedelta import relativedelta
from src.database import SessionLocal
from src.db_models import TransactionDB
from src.forms import TransactionForm
from src.exchange_service import get_usd_rate
from sqlalchemy import func

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

            category=form.category.data.strip().title(),

            transaction_type=form.transaction_type.data,
            
            date=form.date.data
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
    category_spending = (
    session.query(
        TransactionDB.category,
        func.sum(TransactionDB.amount).label("total")
    )
    .filter(TransactionDB.transaction_type == "expense")
    .group_by(TransactionDB.category)
    .order_by(func.sum(TransactionDB.amount).desc())
    .all()
    )

    # ==========================================
    # TOP 5 EXPENSE CATEGORIES
    # ==========================================

    category_spending = (
        session.query(
            TransactionDB.category,
            func.sum(TransactionDB.amount).label("total")
        )
        .filter(
            TransactionDB.transaction_type == "expense"
        )
        .group_by(
            TransactionDB.category
        )
        .order_by(
            func.sum(TransactionDB.amount).desc()
        )
        .limit(5)
        .all()
    )

    category_labels = [
        category
        for category, amount in category_spending
    ]

    category_values = [
        float(amount)
        for category, amount in category_spending
    ]

    # Monthly income vs expense for the last 6 months
    today = date.today()

    monthly_labels = []
    monthly_income_values = []
    monthly_expense_values = []

    for months_ago in range(5, -1, -1):
        target_month = today - relativedelta(months=months_ago)
        month_start = target_month.replace(day=1)
        next_month = month_start + relativedelta(months=1)

        # Calculate total income for this month
        monthly_income = (
            session.query(
                func.sum(TransactionDB.amount)
            )
            .filter(
                TransactionDB.transaction_type == "income",
                TransactionDB.date >= month_start,
                TransactionDB.date < next_month
            )
            .scalar()
        ) or 0

        # Calculate total expense for this month
        monthly_expense = (
            session.query(
                func.sum(TransactionDB.amount)
            )
            .filter(
                TransactionDB.transaction_type == "expense",
                TransactionDB.date >= month_start,
                TransactionDB.date < next_month
            )
            .scalar()
        ) or 0

        # Add month label
        monthly_labels.append(
            target_month.strftime("%b %Y")
        )

        # Add income value
        monthly_income_values.append(
            float(monthly_income)
        )

        # Add expense value
        monthly_expense_values.append(
            float(monthly_expense)
        )

    # Live exchange rate
    usd_rate = get_usd_rate()
    total_spend_usd = total_expense * usd_rate

    session.close()

    return render_template(
        "transactions.html",
        form=form,
        category_labels=category_labels,
        category_values=category_values,
        monthly_labels=monthly_labels,
        monthly_income_values=monthly_income_values,
        monthly_expense_values=monthly_expense_values,
        transactions=all_transactions,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        usd_rate=usd_rate,
        total_spend_usd=total_spend_usd
    )