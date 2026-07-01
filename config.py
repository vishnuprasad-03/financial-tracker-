"""
Configuration settings for the Flask application.
"""


class Config:
    """
    Base configuration class.
    """

    SECRET_KEY = "finance_tracker_secret"

    SQLALCHEMY_DATABASE_URI = "sqlite:///finance.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False