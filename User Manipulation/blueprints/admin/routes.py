from decorators import admin_required
from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_login import current_user, login_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
@admin_required
def admin_dashboard():
    current_app.logger.info(f"Admin {current_user.username} (ID:{current_user.id}) accessed the admin dashboard.")
    return render_template("admin_dashboard.html")