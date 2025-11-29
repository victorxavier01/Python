from decorators import admin_required
from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request
from flask_login import current_user, login_required
from extensions import db
from models import User, Post
from .forms import EditForm
from werkzeug.security import generate_password_hash

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
@admin_required
def admin_dashboard():
    current_app.logger.info(f"Admin {current_user.username} (ID:{current_user.id}) accessed the admin dashboard.")
    return render_template("admin_dashboard.html")

@admin_bp.route("/")
@login_required
@admin_required
def admin_home():
    current_app.logger.info(f"Admin {current_user.username} (ID:{current_user.id}) accessed the admin homepage")
    return render_template("admin_home.html")

@admin_bp.route("/edit_user/", methods=["GET", "POST"])
@login_required
@admin_required
def admin_edit_user():
    current_app.logger.info(f"Admin {current_user.username} (ID:{current_user.id}) accessed the admin edit user page")

    users = db.session.execute(db.select(User)).scalars().all()
    form = EditForm()

    user_id = request.args.get("user_id", type=int)
    selected_user = None

    if user_id:
        selected_user = db.session.get(User, user_id)
        if not selected_user:
            flash("User not found", "danger")
            return redirect(url_for("admin.admin_edit_user"))

    if request.method == "GET" and selected_user:
        form.username.data = selected_user.username
        form.email.data = selected_user.email
        form.profile_pic.data = selected_user.profile_pic

    if request.method == "POST" and form.validate_on_submit() and selected_user:
        current_app.logger.warning(f"Admin {current_user.username} (ID:{current_user.id}) is trying to edit {selected_user.username} (ID:{selected_user.id})")


        selected_user.username = form.username.data
        selected_user.email = form.email.data
        selected_user.profile_pic = form.profile_pic.data

        if form.password.data:
            selected_user.password = generate_password_hash(form.password.data)

        db.session.commit()

        current_app.logger.warning(f"Admin {current_user.username} (ID:{current_user.id}) edited {selected_user.username} (ID:{selected_user.id})")

        flash("User updated successfully!", "success")
        return redirect(url_for("admin.admin_edit_user", user_id = user_id))

    return render_template("admin_edit_user.html", form = form, users = users, selected_user = selected_user)

@admin_bp.route('/delete_user', methods=["GET", "POST"])
@login_required
@admin_required
def delete_user():


    return render_template("delete_user.html", selected_user = selected_user)