from flask import redirect, url_for, flash, current_app, request
from flask_login import current_user
from functools import wraps

def get_user_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = get_user_ip()

        if not current_user.is_authenticated:
            current_app.logger.warning(f"Unauthorized access attempt to admin route by anonymous user. | IP: {ip}")
            flash("Please log in!", "warning")
            return redirect(url_for("user.login"))
        
        if not current_user.is_admin:
            current_app.logger.warning(f"Unauthorized admin access attempt by user {current_user.username} (ID:{current_user.id}) | IP: {ip}")
            flash("You are not allowed!", "danger")
            return redirect(url_for("home.home"))
        
        return f(*args, **kwargs)
    
    return decorated_function