
from flask import (
    Blueprint, request, render_template,
    redirect, url_for, session, flash
)
from datetime import date

from . import db
from .models import Application

applications_bp = Blueprint("applications", __name__)

VALID_STATUSES = [
    "Applied",
    "Online Assessment",
    "Interview",
    "Shortlisted",
    "Rejected",
    "Selected"
]


def logged_in():
    return "user_id" in session


@applications_bp.route("/applications")
def applications():
    if not logged_in():
        return redirect(url_for("auth.login"))

    applications = Application.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "applications.html",
        applications=applications
    )


@applications_bp.route("/add-application", methods=["GET", "POST"])
def add_application():
    if not logged_in():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        status = request.form.get("status", "").strip()
        raw_date = request.form.get("application_date", "").strip()
        notes = request.form.get("notes", "").strip()

        if not company or not role:
            flash("Company name and role cannot be empty.", "error")
            return redirect(url_for("applications.add_application"))

        if status not in VALID_STATUSES:
            flash("Please select a valid application status.", "error")
            return redirect(url_for("applications.add_application"))

        try:
            application_date = date.fromisoformat(raw_date)
        except ValueError:
            flash("Please enter a valid application date.", "error")
            return redirect(url_for("applications.add_application"))

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

        flash("Application added successfully!", "success")
        return redirect(url_for("applications.applications"))

    return render_template("add_application.html")


@applications_bp.route(
    "/applications/edit/<int:application_id>",
    methods=["GET", "POST"]
)
def edit_application(application_id):
    if not logged_in():
        return redirect(url_for("auth.login"))

    application = Application.query.filter_by(
        id=application_id,
        user_id=session["user_id"]
    ).first_or_404()

    if request.method == "POST":
        company = request.form.get("company", "").strip()
        role = request.form.get("role", "").strip()
        status = request.form.get("status", "").strip()
        raw_date = request.form.get("application_date", "").strip()
        notes = request.form.get("notes", "").strip()

        if not company or not role:
            flash("Company name and role cannot be empty.", "error")
            return redirect(url_for(
                "applications.edit_application",
                application_id=application.id
            ))

        if status not in VALID_STATUSES:
            flash("Please select a valid application status.", "error")
            return redirect(url_for(
                "applications.edit_application",
                application_id=application.id
            ))

        try:
            application_date = date.fromisoformat(raw_date)
        except ValueError:
            flash("Please enter a valid application date.", "error")
            return redirect(url_for(
                "applications.edit_application",
                application_id=application.id
            ))

        application.company = company
        application.role = role
        application.status = status
        application.application_date = application_date
        application.notes = notes

        db.session.commit()

        flash("Application updated successfully!", "success")
        return redirect(url_for("applications.applications"))

    return render_template(
        "edit_application.html",
        application=application
    )


@applications_bp.route("/applications/delete/<int:application_id>")
def delete_application(application_id):
    if not logged_in():
        return redirect(url_for("auth.login"))

    application = Application.query.filter_by(
        id=application_id,
        user_id=session["user_id"]
    ).first_or_404()

    db.session.delete(application)
    db.session.commit()

    flash("Application deleted successfully!", "success")
    return redirect(url_for("applications.applications"))
