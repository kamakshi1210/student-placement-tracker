from flask import Flask, request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement_tracker.db"
db = SQLAlchemy(app)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    application_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)


@app.route("/")
def home():
    applications = Application.query.all()
    skills = Skill.query.all()
    applications_count = len(applications)
    interviews_count = Application.query.filter_by(status="Interview").count()
    rejected_count = Application.query.filter_by(status="Rejected").count()
    applied_count = Application.query.filter_by(status="Applied").count()
    assessment_count = Application.query.filter_by(status="Online Assessment").count()
    shortlisted_count = Application.query.filter_by(status="Shortlisted").count()
    selected_count = Application.query.filter_by(status="Selected").count()
    recent_applications = Application.query.order_by(Application.application_date.desc()).limit(5).all()

    return render_template(
        "home.html",
        name="Kamakshi",
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


@app.route("/add_skill",methods=["GET","POST"])
def add_skill():
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
            level=level
        )
        db.session.add(skill)
        db.session.commit()
        return redirect(url_for("skills"))
    return render_template("add_skill.html")

@app.route("/skills")
def skills():
    skills = Skill.query.all()
    return render_template("skills.html",skills=skills)

@app.route("/edit-skill/<int:skill_id>", methods=["GET", "POST"])
def edit_skill(skill_id):
    skill = Skill.query.get(skill_id)
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
    skill = Skill.query.get(skill_id)

    if skill is None:
        return "Skill not found", 404

    db.session.delete(skill)
    db.session.commit()

    return redirect(url_for("skills"))

@app.route("/applications")
def applications():
    applications = Application.query.all()
    return render_template(
        "applications.html",
        applications=applications
    )

@app.route("/add-application", methods=["GET", "POST"])
def add_application():
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
            notes=notes
        )
        db.session.add(application)
        db.session.commit()
        return redirect(url_for("applications"))
    
    return render_template("add_application.html")

@app.route("/applications/edit/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):
    application = db.get_or_404(Application, application_id)
    if application is None:
        return "Application not found", 404
    if request.method == "POST":
        application.company = request.form["company"]
        application.role = request.form["role"]
        application.status = request.form["status"]
        application.application_date = date.fromisoformat(
            request.form["application_date"]
        )
        application.notes = request.form["notes"]

        db.session.commit()
        return redirect(url_for("applications"))

    return render_template(
        "edit_application.html",
        application=application
    )

@app.route("/applications/delete/<int:application_id>")
def delete_application(application_id):
    application = db.get_or_404(Application, application_id)
    if application is None:
        return "appliation not found", 404

    db.session.delete(application)
    db.session.commit()

    return redirect(url_for("applications"))

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)