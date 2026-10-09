
from flask import (
    Blueprint, request, render_template,
    redirect, url_for, session, flash
)

from . import db
from .models import Skill

skills_bp = Blueprint("skills", __name__)

VALID_LEVELS = ["Beginner", "Intermediate", "Advanced"]


def logged_in():
    return "user_id" in session


@skills_bp.route("/skills")
def skills():
    if not logged_in():
        return redirect(url_for("auth.login"))

    skills = Skill.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template("skills.html", skills=skills)


@skills_bp.route("/add_skill", methods=["GET", "POST"])
def add_skill():
    if not logged_in():
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        skill_name = request.form.get("skill_name", "").strip()
        category = request.form.get("category", "").strip()
        level = request.form.get("level", "").strip()

        if not skill_name or not category:
            flash("Skill name and category cannot be empty.", "error")
            return redirect(url_for("skills.add_skill"))

        if level not in VALID_LEVELS:
            flash("Please select a valid skill level.", "error")
            return redirect(url_for("skills.add_skill"))

        skill = Skill(
            name=skill_name,
            category=category,
            level=level,
            user_id=session["user_id"]
        )

        db.session.add(skill)
        db.session.commit()

        flash("Skill added successfully!", "success")
        return redirect(url_for("skills.skills"))

    return render_template("add_skill.html")


@skills_bp.route("/edit-skill/<int:skill_id>", methods=["GET", "POST"])
def edit_skill(skill_id):
    if not logged_in():
        return redirect(url_for("auth.login"))

    skill = Skill.query.filter_by(
        id=skill_id,
        user_id=session["user_id"]
    ).first_or_404()

    if request.method == "POST":
        skill_name = request.form.get("skill_name", "").strip()
        category = request.form.get("category", "").strip()
        level = request.form.get("level", "").strip()

        if not skill_name or not category:
            flash("Skill name and category cannot be empty.", "error")
            return redirect(url_for("skills.edit_skill", skill_id=skill.id))

        if level not in VALID_LEVELS:
            flash("Please select a valid skill level.", "error")
            return redirect(url_for("skills.edit_skill", skill_id=skill.id))

        skill.name = skill_name
        skill.category = category
        skill.level = level

        db.session.commit()

        flash("Skill updated successfully!", "success")
        return redirect(url_for("skills.skills"))

    return render_template("edit_skill.html", skill=skill)


@skills_bp.route("/delete-skill/<int:skill_id>")
def delete_skill(skill_id):
    if not logged_in():
        return redirect(url_for("auth.login"))

    skill = Skill.query.filter_by(
        id=skill_id,
        user_id=session["user_id"]
    ).first_or_404()

    db.session.delete(skill)
    db.session.commit()

    flash("Skill deleted successfully!", "success")
    return redirect(url_for("skills.skills"))
