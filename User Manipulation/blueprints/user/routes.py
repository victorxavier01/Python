from flask import Blueprint, render_template
from flask_login import current_user

user_bp = Blueprint("user", __name__)

@user_bp.route('/login', methods=["GET", "LOGIN"])
def login():
    return render_template("login.html")