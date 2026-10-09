
from flask import (
    Blueprint, request, render_template,
    redirect, url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        if not name:
            flash("Name cannot be empty.", "error")
            return redirect(url_for("auth.register"))

        if not email:
            flash("Email cannot be empty.", "error")
            return redirect(url_for("auth.register"))

        if not password.strip():
            flash("Password cannot be empty.", "error")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered.", "error")
            return redirect(url_for("auth.register"))

        password_hash = generate_password_hash(password)

        user = User(
            name=name,
            email=email,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        if not email or not password:
            flash("Enter both email and password.", "error")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("main.home"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
