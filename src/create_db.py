"""
Create the SQLite database and tables.
"""

from src.database import engine, Base
from src.db_models import TransactionDB

Base.metadata.create_all(bind=engine)

print("Database initialization completed.")