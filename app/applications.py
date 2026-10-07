from flask import Blueprint, request, render_template, redirect, url_for, session
from datetime import date

from . import db
from .models import Application

applications_bp = Blueprint("applications", __name__)

@applications_bp.route("/applications")
def applications():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    applications = Application.query.filter_by(user_id=session["user_id"]).all()
    return render_template(
        "applications.html",
        applications=applications
    )

@applications_bp.route("/add-application", methods=["GET", "POST"])
def add_application():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
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
        return redirect(url_for("applications.applications"))
    
    return render_template("add_application.html")

@applications_bp.route("/applications/edit/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
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
        return redirect(url_for("applications.applications"))

    return render_template(
        "edit_application.html",
        application=application
    )

@applications_bp.route("/applications/delete/<int:application_id>")
def delete_application(application_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    application = Application.query.filter_by(id=application_id,user_id=session["user_id"]).first_or_404()
    if application is None:
        return "appliation not found", 404

    db.session.delete(application)
    db.session.commit()

    return redirect(url_for("applications.applications"))
