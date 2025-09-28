from flask import Blueprint, render_template
from flask_login import current_user
from forms import RegisterForm, LoginForm

user_bp = Blueprint("user", __name__)

@user_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)