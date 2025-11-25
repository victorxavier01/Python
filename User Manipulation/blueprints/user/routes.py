from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_login import current_user, login_user
from .forms import RegisterForm, LoginForm
from werkzeug.security import check_password_hash
from extensions import db
from models import User

user_bp = Blueprint("user", __name__)

@user_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.home"))
    form = LoginForm()

    if form.validate_on_submit():
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()

        if not user:
            flash("That email does not exist.")
            return redirect(url_for("user.login"))
        
        elif not check_password_hash(user.password, password):
            flash("Wrong password")
            return redirect(url_for("user.login"))
        
        else:
            login_user(user)
            #return redirect(url_for(get_all_posts))
            return redirect(url_for("home.home"))
        
    current_app.logger.info("Usuário acessou a página de login")
    return render_template("login.html", form=form)

@user_bp.route('/register', methods=["GET", "POST"])
def register():
    current_app.logger.info("Usuário acessou a página de registro")
    return render_template("register.html")