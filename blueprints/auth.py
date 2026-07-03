from flask import Blueprint, render_template, request, redirect, url_for

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

auth_bp = Blueprint(
    "auth",
    __name__
)

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]

    password = request.form["password"]

    session = SessionLocal()

    existing_user = (
        session.query(UserDB)
        .filter_by(username=username)
        .first()
    )

    if existing_user:

        session.close()

        return "Username already exists."

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

    return redirect(url_for("auth.login"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    session = SessionLocal()

    user = (
        session.query(UserDB)
        .filter_by(username=username)
        .first()
    )

    if user is None:
        session.close()
        return "Invalid username."

    if not check_password_hash(user.password_hash, password):
        session.close()
        return "Invalid password."

    login_user(
    user,
    remember=True
)

    session.close()

    return redirect(url_for("transactions.transactions"))

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("auth.login"))