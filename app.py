"""
Main Flask application.
"""

from flask import Flask, render_template
from flask_login import LoginManager

from config import Config
from blueprints.transactions import transactions_bp
from blueprints.api import api_bp
from blueprints.auth import auth_bp
from blueprints.file_operations import file_operations_bp
from src.database import SessionLocal
from src.db_models import UserDB
from blueprints.health import health_bp
from src.scheduler import start_scheduler
from dotenv import load_dotenv
import os

from src.extensions import limiter

load_dotenv()

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    session = SessionLocal()

    user = session.get(
        UserDB,
        int(user_id)
    )

    session.close()

    return user


def create_app():
    """
    Create and configure the Flask application.
    """

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.config.from_object(Config)
    
    limiter.init_app(app)
        
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @app.route("/")
    def home():
        return "Finance Tracker is Running 🚀"

    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(file_operations_bp)
    app.register_blueprint(health_bp)

    @app.errorhandler(429)
    def ratelimit_handler(error):

        return (
        render_template(
            "429.html"
        ),
        429
    )

    return app


app = create_app()


if __name__ == "__main__":

    start_scheduler()

    app.run(
        debug=True,
        use_reloader=False
    )

