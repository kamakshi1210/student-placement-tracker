import os
from dotenv import load_dotenv
from flask import Flask, request,render_template,redirect,url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app=Flask(__name__)

secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise ValueError("SECRET_KEY is not set.")
app.secret_key = secret_key

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    application_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

@app.route("/register", methods=["GET", "POST"])
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

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for("home"))
        return "Invalid email or password"

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("user_id", None)

    return redirect(url_for("login"))

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = User.query.get(session["user_id"])
    if not user:
        session.pop("user_id", None)
        return redirect(url_for("login"))
    
    applications = Application.query.filter_by(user_id=session["user_id"]).all()
    skills = Skill.query.filter_by(user_id=session["user_id"]).all()
    applications_count = len(applications)
    interviews_count = Application.query.filter_by(
        status="Interview",
        user_id=session["user_id"]
    ).count()

    rejected_count = Application.query.filter_by(
        status="Rejected",
        user_id=session["user_id"]
    ).count()

    applied_count = Application.query.filter_by(
        status="Applied",
        user_id=session["user_id"]
    ).count()

    assessment_count = Application.query.filter_by(
        status="Online Assessment",
        user_id=session["user_id"]
    ).count()

    shortlisted_count = Application.query.filter_by(
        status="Shortlisted",
        user_id=session["user_id"]
    ).count()

    selected_count = Application.query.filter_by(
        status="Selected",
        user_id=session["user_id"]
    ).count()
    recent_applications = Application.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Application.application_date.desc()
    ).limit(5).all()

    return render_template(
        "home.html",
        name=user.name,
        applications_count=applications_count,
        interviews_count=interviews_count,
        rejected_count=rejected_count,
        applied_count=applied_count,
        assessment_count=assessment_count,
        shortlisted_count=shortlisted_count,
        selected_count=selected_count,
        skills=skills,
        recent_applications=recent_applications
    )


@app.route("/skills")
def skills():
    if "user_id" not in session:
        return redirect(url_for("login"))
    skills = Skill.query.filter_by(user_id=session["user_id"]).all()
    return render_template("skills.html",skills=skills)

@app.route("/add_skill",methods=["GET","POST"])
def add_skill():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method=="POST":
        skill_name=request.form["skill_name"]
        level=request.form["level"]
        category=request.form["category"]
        if skill_name == "":
            return "Skill name cannot be empty."
        if level not in ["Beginner","Intermediate","Advanced"]:
            return "invalid level"
        skill = Skill(
            name=skill_name,
            category=category,
            level=level,
            user_id=session["user_id"]
        )
        db.session.add(skill)
        db.session.commit()
        return redirect(url_for("skills"))
    return render_template("add_skill.html")

@app.route("/edit-skill/<int:skill_id>", methods=["GET", "POST"])
def edit_skill(skill_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    skill = Skill.query.filter_by(id=skill_id,user_id=session["user_id"]).first_or_404()
    if skill is None:
        return "Skill not found", 404
    if request.method == "POST":
        skill.name = request.form["skill_name"]
        skill.category = request.form["category"]
        skill.level = request.form["level"]
        db.session.commit()
        return redirect(url_for("skills"))

    return render_template("edit_skill.html", skill=skill)

@app.route("/delete-skill/<int:skill_id>")
def delete_skill(skill_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    skill = Skill.query.filter_by(id=skill_id,user_id=session["user_id"]).first_or_404()

    if skill is None:
        return "Skill not found", 404

    db.session.delete(skill)
    db.session.commit()

    return redirect(url_for("skills"))

@app.route("/applications")
def applications():
    if "user_id" not in session:
        return redirect(url_for("login"))
    applications = Application.query.filter_by(user_id=session["user_id"]).all()
    return render_template(
        "applications.html",
        applications=applications
    )

@app.route("/add-application", methods=["GET", "POST"])
def add_application():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]
        raw_date = request.form.get("application_date", "").strip()
        notes = request.form["notes"]
        if company == "":
            return "company name cannot be empty."
        if status not in ["Applied","Online Assessment","Interview","Shortlisted","Rejected","Selected"]:
            return "invalid status"
        if not raw_date:
            return "Application date cannot be empty.", 400

        # Safely attempt date parsing
        try:
            application_date = date.fromisoformat(raw_date)
        except ValueError:
            return "Invalid date format. Expected YYYY-MM-DD.", 400
        application = Application(
            company=company,
            role=role,
            status=status,
            application_date=application_date,
            notes=notes,
            user_id=session["user_id"]
        )
        db.session.add(application)
        db.session.commit()
        return redirect(url_for("applications"))
    
    return render_template("add_application.html")

@app.route("/applications/edit/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    application = Application.query.filter_by(id=application_id,user_id=session["user_id"]).first_or_404()
    if application is None:
        return "Application not found", 404
    if request.method == "POST":
        company = request.form["company"].strip()
        role = request.form["role"].strip()

        if company == "":
            return "Company name cannot be empty.", 400

        if role == "":
            return "Role cannot be empty.", 400

        application.company = company
        application.role = role
        status = request.form["status"]
        if status not in ["Applied", "Online Assessment", "Interview", "Shortlisted", "Rejected", "Selected"]:
            return "Invalid status.", 400
        application.status = status
        raw_date = request.form.get("application_date", "").strip()
        if not raw_date:
            return "Application date cannot be empty.", 400
        try:
            application.application_date = date.fromisoformat(raw_date)
        except ValueError:
            return "Invalid date format. Expected YYYY-MM-DD.", 400
        application.notes = request.form["notes"]

        db.session.commit()
        return redirect(url_for("applications"))

    return render_template(
        "edit_application.html",
        application=application
    )

@app.route("/applications/delete/<int:application_id>")
def delete_application(application_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    application = Application.query.filter_by(id=application_id,user_id=session["user_id"]).first_or_404()
    if application is None:
        return "appliation not found", 404

    db.session.delete(application)
    db.session.commit()

    return redirect(url_for("applications"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

