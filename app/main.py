from flask import Blueprint, render_template, redirect, url_for, session

from .models import User, Skill, Application

main = Blueprint("main", __name__)

@main.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    user = User.query.get(session["user_id"])
    if not user:
        session.pop("user_id", None)
        return redirect(url_for("auth.login"))
    
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

@main.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
