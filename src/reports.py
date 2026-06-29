"""
Reports for Finance Tracker.
"""

from sqlalchemy import func

from src.database import SessionLocal
from src.db_models import TransactionDB

def category_summary():
    """
    Return the top 3 spending categories.
    """

    session = SessionLocal()
    
    summary = (
    session.query(
        TransactionDB.category,
        func.sum(TransactionDB.amount).label("total_spent")
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
    .limit(3)
    .all()
)

    session.close()

    return summary