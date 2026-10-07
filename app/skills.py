from flask import Blueprint, request, render_template, redirect, url_for, session

from . import db
from .models import Skill

skills_bp = Blueprint("skills", __name__)

@skills_bp.route("/skills")
def skills():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    skills = Skill.query.filter_by(user_id=session["user_id"]).all()
    return render_template("skills.html",skills=skills)

@skills_bp.route("/add_skill",methods=["GET","POST"])
def add_skill():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
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
        return redirect(url_for("skills.skills"))
    return render_template("add_skill.html")

@skills_bp.route("/edit-skill/<int:skill_id>", methods=["GET", "POST"])
def edit_skill(skill_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    skill = Skill.query.filter_by(id=skill_id,user_id=session["user_id"]).first_or_404()
    if skill is None:
        return "Skill not found", 404
    if request.method == "POST":
        skill.name = request.form["skill_name"]
        skill.category = request.form["category"]
        skill.level = request.form["level"]
        db.session.commit()
        return redirect(url_for("skills.skills"))

    return render_template("edit_skill.html", skill=skill)

@skills_bp.route("/delete-skill/<int:skill_id>")
def delete_skill(skill_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    skill = Skill.query.filter_by(id=skill_id,user_id=session["user_id"]).first_or_404()

    if skill is None:
        return "Skill not found", 404

    db.session.delete(skill)
    db.session.commit()

    return redirect(url_for("skills.skills"))
