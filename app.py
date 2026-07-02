"""
Main Flask application.
"""

from flask import Flask

from config import Config
from blueprints.transactions import transactions_bp
from blueprints.api import api_bp


def create_app():
    """
    Create and configure the Flask application.
    """

    app = Flask(__name__)

    app.config.from_object(Config)

    @app.route("/")
    def home():
        return "Finance Tracker is Running 🚀"
    
    app.register_blueprint(transactions_bp)
    app.register_blueprint(api_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)