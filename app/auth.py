from flask import Blueprint, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        if name.strip() == "":
            return "Name cannot be empty."

        if email.strip() == "":
            return "Email cannot be empty."

        if password.strip() == "":
            return "Password cannot be empty."
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered."
        password_hash = generate_password_hash(password)

        user = User(
            name=name,
            email=email,
            password_hash=password_hash
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        if email.strip() == "":
            return "Email cannot be empty."

        if password.strip() == "":
            return "Password cannot be empty."

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect(url_for("main.home"))
        return "Invalid email or password"

    return render_template("login.html")

@auth.route("/logout")
def logout():

    session.pop("user_id", None)

    return redirect(url_for("auth.login"))
