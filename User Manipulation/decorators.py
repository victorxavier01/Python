from flask import redirect, url_for, flash
from flask_login import current_user
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in!", "warning")
            return redirect(url_for("user.login"))
        if not current_user.is_admin:
            flash("You are not allowed on this page!", "danger")
            return redirect(url_for("home.home"))
        return f(*args, **kwargs)
    return decorated_function