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

    # 1. Read filter parameters
    category_filter = request.args.get(
        "category",
        "",
        type=str
    ).strip()

    start_date_filter = request.args.get(
        "start_date",
        "",
        type=str
    ).strip()

    end_date_filter = request.args.get(
        "end_date",
        "",
        type=str
    ).strip()

    page = request.args.get(
        "page",
        1,
        type=int
    )

    if page < 1:
        page = 1

    per_page = 10


    # 2. Handle Add Transaction form
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


    # 3. Get ALL transactions
    all_transactions = session.query(
        TransactionDB
    ).all()


    # 4. Calculate dashboard totals
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


    # 5. Create filtered query
    filtered_query = session.query(
        TransactionDB
    )

    if category_filter:
        filtered_query = filtered_query.filter(
            TransactionDB.category == category_filter
        )


    # 6. Start date filter
    if start_date_filter:

        try:
            start_date_value = date.fromisoformat(
                start_date_filter
            )

            filtered_query = filtered_query.filter(
                TransactionDB.date >= start_date_value
            )

        except ValueError:
            start_date_filter = ""


    # 7. End date filter
    if end_date_filter:

        try:
            end_date_value = date.fromisoformat(
                end_date_filter
            )

            filtered_query = filtered_query.filter(
                TransactionDB.date <= end_date_value
            )

        except ValueError:
            end_date_filter = ""


    # 8. Pagination
    filtered_query = filtered_query.order_by(
    TransactionDB.id.asc()
    )

    total_filtered_transactions = filtered_query.count()

    total_pages = max(
        1,
        (
            total_filtered_transactions
            + per_page
            - 1
        ) // per_page
    )

    if page > total_pages:
        page = total_pages

    paginated_transactions = (
        filtered_query
        .offset((page - 1) * per_page)
        .limit(per_page)
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
        paginated_transactions=paginated_transactions,
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        usd_rate=usd_rate,
        total_spend_usd=total_spend_usd,
        category_filter=category_filter,
        start_date_filter=start_date_filter,
        end_date_filter=end_date_filter,
        page=page,
        total_pages=total_pages,
        total_filtered_transactions=total_filtered_transactions,
    )