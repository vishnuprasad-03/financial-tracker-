"""
Database models for Finance Tracker.
"""

from sqlalchemy import Column, Integer, Float, String

from src.database import Base
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float


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

class BudgetDB(Base):
    """
    Database model for monthly budgets.
    """

    __tablename__ = "budgets"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    category = Column(
        String,
        unique=True,
        nullable=False
    )

    monthly_limit = Column(
        Float,
        nullable=False
    )

class UserDB(Base, UserMixin):
    """
    Database model for users.
    """

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )