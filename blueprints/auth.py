from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from src.database import SessionLocal
from src.db_models import UserDB

from src.extensions import limiter

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def register():

    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"].strip()

    password = request.form["password"]

    session = SessionLocal()

    existing_user = (
        session.query(UserDB)
        .filter_by(username=username)
        .first()
    )

    if existing_user:

        session.close()

        flash(
            "Username already exists.",
            "danger"
        )

        return redirect(
            url_for("auth.register")
        )

    hashed_password = generate_password_hash(
        password,
        method="pbkdf2:sha256"
    )

    user = UserDB(

        username=username,

        password_hash=hashed_password

    )

    session.add(user)

    session.commit()

    session.close()

    flash(
        "Registration successful! Please login.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"].strip()

    password = request.form["password"]

    session = SessionLocal()

    user = (
        session.query(UserDB)
        .filter_by(username=username)
        .first()
    )

    if user is None:

        session.close()

        flash(
            "Invalid username or password.",
            "danger"
            )

    return render_template(
    "login.html",
        username=username
        )

    if not check_password_hash(
        user.password_hash,
        password
    ):

        session.close()

        flash(
    "Invalid username or password.",
    "danger"
    )

    return render_template(
    "login.html",
    username=username
    )
    

    login_user(
        user,
        remember=True
    )

    session.close()

    flash(
        f"Welcome back, {user.username}!",
        "success"
    )

    return redirect(
        url_for("transactions.transactions")
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )