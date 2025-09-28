from flask import Blueprint, render_template
from flask_login import current_user

home_bp = Blueprint("home", __name__)

@home_bp.route('/')
def home():
    #, logged_in=current_user.current_user.is_authenticated
    return render_template("index.html")