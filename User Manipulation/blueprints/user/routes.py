from flask import Blueprint, render_template, current_app
from flask_login import current_user
#from forms import RegisterForm, LoginForm

user_bp = Blueprint("user", __name__)

@user_bp.route('/login', methods=["GET", "POST"])
def login():
    #form = LoginForm()
    current_app.logger.info("Usuário acessou a página de login")
    return render_template("login.html")

@user_bp.route('/register', methods=["GET", "POST"])
def register():
    current_app.logger.info("Usuário acessou a página de registro")
    return render_template("register.html")