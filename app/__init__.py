import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise ValueError("SECRET_KEY is not set.")
    app.secret_key = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    db.init_app(app)
    from .auth import auth
    from .skills import skills_bp
    from .applications import applications_bp
    from .main import main

    app.register_blueprint(auth)
    app.register_blueprint(skills_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(main)

    return app

