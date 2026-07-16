"""
Health-check endpoint for Finance Tracker.
"""

from flask import Blueprint, jsonify
from sqlalchemy import text

from src.database import SessionLocal


health_bp = Blueprint(
    "health",
    __name__
)


@health_bp.route("/api/health")
def health_check():
    """
    Check whether the Flask application and database
    are running correctly.
    """

    db_session = SessionLocal()

    try:
        # Test database connection
        db_session.execute(text("SELECT 1"))

        return jsonify({
            "status": "healthy",
            "service": "finance-tracker",
            "database": "connected"
        }), 200

    except Exception as error:

        print(
            f"Health check failed: {error}"
        )

        return jsonify({
            "status": "unhealthy",
            "service": "finance-tracker",
            "database": "disconnected"
        }), 503

    finally:
        db_session.close()