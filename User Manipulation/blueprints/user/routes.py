from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from .forms import RegisterForm, LoginForm, PostForm
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from models import User, Post
from .utils import save_profile_pic
from datetime import date

user_bp = Blueprint("user", __name__)

@user_bp.route('/login', methods=["GET", "POST"])
def login():
    current_app.logger.info("Usuário acessou a página de login")
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
        
    return render_template("login.html", form=form)

@user_bp.route('/register', methods=["GET", "POST"])
def register():
    current_app.logger.info("Usuário acessou a página de registro")
    form = RegisterForm()

    if form.validate_on_submit():
        current_app.logger.info("Iniciando processo de cadastro!")
        user_check = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()

        if user_check:
            print("aaaa")
            flash("Email already exists. Try logging in instead!")
            return redirect(url_for("user.login"))

        username_check = db.session.execute(
            db.select(User).where(User.username == form.username.data)).scalar()

        if username_check:
            print("bbbb")
            flash("Username already taken.")
            return redirect(url_for("user.register"))

        picture_file = None
        if form.profile_pic.data:
            print("cccc")
            picture_file = save_profile_pic(form.profile_pic.data)

        new_user = User(
            username = form.username.data,
            email = form.email.data,
            password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8),
            profile_pic = picture_file or "default.png"
        )

        db.session.add(new_user)
        db.session.commit()

        current_app.logger.info("Account created successfully!\nReturning to Home page.")
        login_user(new_user)
        return redirect(url_for("home.home"))
    
    return render_template("register.html", form=form)

@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    current_app.logger.info("User has logged out.")
    return redirect(url_for("home.home"))

@user_bp.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    current_app.logger.info("User has entered create poster page")
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title = form.title.data,
            date = date.today().strftime("%B %d, %Y"),
            body = form.body.data,
            author = current_user.id,
            author_name = current_user.username
        )
        db.session.add(new_post)
        db.session.commit()
        current_app.logger.info("Post created successfully!")
        #return redirect(url_for(get_all_posts))
        return redirect(url_for("home.home"))


    return render_template("create-post.html", form=form)