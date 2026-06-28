"""
Database models for Finance Tracker.
"""

from sqlalchemy import Column, Integer, Float, String

from src.database import Base


class TransactionDB(Base):
    """
    Database model for transactions.
    """

    __tablename__ = "transactions"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    amount = Column(
        Float,
        nullable=False
    )

    category = Column(
        String,
        nullable=False
    )

    transaction_type = Column(
        String,
        nullable=False
    )