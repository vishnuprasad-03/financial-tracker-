"""
Background task scheduler for Finance Tracker.
"""

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date

from dateutil.relativedelta import relativedelta
from sqlalchemy import func

from src.database import SessionLocal
from src.db_models import TransactionDB

import os
import smtplib

from email.message import EmailMessage

scheduler = BackgroundScheduler()


def test_background_task():
    """
    Simple test task to verify that APScheduler is working.
    """

    print(
        "Background task is running successfully!"
    )

def check_monthly_budget():
    """
    Calculate current month's expenses and compare them
    against the configured monthly budget.
    """

    monthly_budget = 10000.0

    today = date.today()

    month_start = today.replace(day=1)

    next_month = month_start + relativedelta(months=1)

    db_session = SessionLocal()

    try:
        monthly_expense = (
            db_session.query(
                func.sum(TransactionDB.amount)
            )
            .filter(
                TransactionDB.transaction_type == "expense",
                TransactionDB.date >= month_start,
                TransactionDB.date < next_month
            )
            .scalar()
        ) or 0

        monthly_expense = float(monthly_expense)

        print(
            f"Monthly budget: ₹{monthly_budget:.2f}"
        )

        print(
            f"Current monthly spending: ₹{monthly_expense:.2f}"
        )

        if monthly_expense > monthly_budget:

            exceeded_amount = (
            monthly_expense - monthly_budget
            )

            print(
                "⚠️ Budget exceeded by "
                f"₹{exceeded_amount:.2f}"  )

            send_budget_alert_email(
                monthly_budget,
                monthly_expense,
                exceeded_amount
            )

        else:

            remaining_budget = (
                monthly_budget - monthly_expense
            )

            print(
                "✅ Budget remaining: "
                f"₹{remaining_budget:.2f}"
            )

    except Exception as error:

        print(
            f"Budget check failed: {error}"
        )

    finally:

        db_session.close()

def send_budget_alert_email(
    monthly_budget,
    monthly_expense,
    exceeded_amount
):
    """
    Send an email alert when monthly spending
    exceeds the configured budget.
    """

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = os.getenv("ALERT_EMAIL")

    if not all([
        sender_email,
        sender_password,
        receiver_email
    ]):
        print(
            "Budget alert email skipped: "
            "email environment variables are missing."
        )
        return

    message = EmailMessage()

    message["Subject"] = (
        "Finance Tracker - Monthly Budget Alert"
    )

    message["From"] = sender_email
    message["To"] = receiver_email

    message.set_content(
        f"""
Your monthly spending has exceeded your budget.

Monthly Budget: ₹{monthly_budget:.2f}
Current Spending: ₹{monthly_expense:.2f}
Amount Exceeded: ₹{exceeded_amount:.2f}

Please review your recent transactions.

Finance Tracker
        """.strip()
    )

    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                sender_email,
                sender_password
            )

            smtp.send_message(message)

        print(
            "Budget alert email sent successfully!"
        )

    except Exception as error:

        print(
            f"Failed to send budget alert email: {error}"
        )

def start_scheduler():
    """
    Start APScheduler and register background jobs.
    """
    print(os.getenv("EMAIL_ADDRESS"))
    print(os.getenv("ALERT_EMAIL"))
    print(os.getenv("SECRET_KEY"))

    scheduler.add_job(
        check_monthly_budget,
        trigger="cron",
        day=1,
        hour=9,
        minute=0,
        id="monthly_budget_check",
        replace_existing=True
    )

    scheduler.start()

    print("APScheduler started successfully!")

   
