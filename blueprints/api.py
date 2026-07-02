"""
REST API routes.
"""

from flask import Blueprint, jsonify

from src.database import SessionLocal
from src.db_models import TransactionDB
from flask import Blueprint, jsonify, request

api_bp = Blueprint(
    "api",
    __name__
)


@api_bp.route(
    "/api/transactions",
    methods=["GET"]
)
def get_transactions():
    """
    Return all transactions.
    """

    session = SessionLocal()

    transactions = session.query(
        TransactionDB
    ).all()

    session.close()

    result = []

    for transaction in transactions:

        result.append({

            "id": transaction.id,

            "amount": transaction.amount,

            "category": transaction.category,

            "transaction_type": transaction.transaction_type

        })

    return jsonify(result), 200

@api_bp.route(
    "/api/transactions",
    methods=["POST"]
)
def create_transaction():
    """
    Create a new transaction.
    """

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Invalid JSON data."
        }), 400

    session = SessionLocal()

    transaction = TransactionDB(

        amount=data["amount"],

        category=data["category"],

        transaction_type=data["transaction_type"]

    )

    session.add(transaction)

    session.commit()

    session.refresh(transaction)

    session.close()

    return jsonify({

        "message": "Transaction created successfully.",

        "id": transaction.id

    }), 201

@api_bp.route(
    "/api/transactions/<int:transaction_id>",
    methods=["DELETE"]
)
def delete_transaction(transaction_id):
    """
    Delete a transaction.
    """

    session = SessionLocal()

    transaction = session.get(
        TransactionDB,
        transaction_id
    )

    if transaction is None:

        session.close()

        return jsonify({

            "error": "Transaction not found."

        }), 404

    session.delete(transaction)

    session.commit()

    session.close()

    return jsonify({

        "message": "Transaction deleted successfully."

    }), 200