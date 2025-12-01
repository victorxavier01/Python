from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from .forms import RegisterForm, LoginForm, PostForm, EditPostForm, CommentForm
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from models import User, Post, Likes, Comments
from .utils import save_profile_pic, save_post_pic
from datetime import datetime
from zoneinfo import ZoneInfo

user_bp = Blueprint("user", __name__, url_prefix="/user")

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
            return redirect(url_for("user.see_all_posts"))
        
    return render_template("login.html", form=form)

@user_bp.route('/register', methods=["GET", "POST"])
def register():
    current_app.logger.info("Usuário acessou a página de registro")

    form = RegisterForm()

    if form.validate_on_submit():
        current_app.logger.info("Iniciando processo de cadastro!")
        user_check = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()

        if user_check:
            flash("Email already exists. Try logging in instead!")
            return redirect(url_for("user.login"))

        username_check = db.session.execute(
            db.select(User).where(User.username == form.username.data)).scalar()

        if username_check:
            flash("Username already taken.")
            return redirect(url_for("user.register"))

        picture_file = None
        if form.profile_pic.data:
            picture_file = save_profile_pic(form.profile_pic.data)

        new_user = User(
            username = form.username.data,
            email = form.email.data,
            password = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8),
            profile_pic = picture_file or "default.png"
        )

        db.session.add(new_user)
        db.session.commit()

        current_app.logger.info(f"Account {new_user.username} (ID:{new_user.id}) created successfully! Returning to Home page.")

        login_user(new_user)

        return redirect(url_for("home.home"))
    
    return render_template("register.html", form=form)

@user_bp.route("/logout")
@login_required
def logout():
    current_app.logger.info(f"User {current_user.username} (ID:{current_user.id}) has logged out")
    logout_user()
    return redirect(url_for("home.home"))

@user_bp.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    current_app.logger.info(f"User {current_user.username} (ID:{current_user.id}) accessed the create post page.")
    form = PostForm()

    if form.validate_on_submit():
        if form.post_pic.data:
            picture_file = save_post_pic(form.post_pic.data)
        else:
            picture_file = "default.png"

        new_post = Post(
            title = form.title.data,
            date = datetime.now(ZoneInfo("America/Sao_Paulo")),
            body = form.body.data,
            user_id = current_user.id,
            post_pic = picture_file,
        )
        
        db.session.add(new_post)
        db.session.commit()

        current_app.logger.info("Post created successfully!")

        return redirect(url_for("user.see_post", post_id = new_post.id))

    return render_template("create_post.html", form = form)

@user_bp.route("/my_profile", methods=["GET", "POST"])
@login_required
def my_profile():
    user_posts = Post.query.filter_by(user_id = current_user.id).all()

    return render_template("my_profile.html", posts = user_posts)

@user_bp.route("/see_post/<int:post_id>", methods=["GET", "POST"])
@login_required
def see_post(post_id):
    form = CommentForm()

    post_to_see = Post.query.get_or_404(post_id)
    
    if form.validate_on_submit():
        new_comment = Comments(
            user_id = current_user.id,
            post_id = post_id,
            body = form.body.data,
            date = datetime.now(ZoneInfo("America/Sao_Paulo")),
        )

        db.session.add(new_comment)
        db.session.commit()

        current_app.logger.info(f"{current_user.username} (ID:{current_user.id}) has commented on {post_to_see.author.username}'s post ID: {post_to_see.id}")

        flash("Comment added!", "success")

        return redirect(url_for("user.see_post", post_id = post_id))
    
    return render_template("see_post.html", post = post_to_see, form = form)

@user_bp.route("/see_all_posts", methods=["GET", "POST"])
@login_required
def see_all_posts():
    form = CommentForm()

    posts = Post.query.order_by(Post.date.desc()).all()

    if form.validate_on_submit():
        post_id = int(form.post_id.data)
        post_to_see = Post.query.get_or_404(post_id)

        new_comment = Comments(
            user_id = current_user.id,
            post_id = post_id,
            body = form.body.data,
            date = datetime.now(ZoneInfo("America/Sao_Paulo")),
        )

        db.session.add(new_comment)
        db.session.commit()

        current_app.logger.info(f"{current_user.username} (ID:{current_user.id}) has commented on {post_to_see.author.username}'s post ID: {post_to_see.id}")

        flash("Comment added!", "success")

        return redirect(url_for("user.see_post", post_id = post_id))

    return render_template("see_all_posts.html", posts=posts, form=form)

@user_bp.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    form = EditPostForm()

    post_to_edit = Post.query.get_or_404(post_id)

    if post_to_edit.user_id != current_user.id and not current_user.is_admin:
        flash("You have not permission to edit this post", "danger")
        current_app.logger.warning(f"User {current_user.username} (ID:{current_user.id}) tried to edit post {post_id} without permission")
        return redirect(url_for("home.home"))

    if form.validate_on_submit():
        post_to_edit.title = form.title.data
        post_to_edit.body = form.body.data
        post_to_edit.date = datetime.now(ZoneInfo("America/Sao_Paulo"))
        
        if form.post_pic.data:
            picture_file = save_post_pic(form.post_pic.data)
            post_to_edit.post_pic = picture_file

        current_app.logger.info(f"User {current_user.username} (ID:{current_user.id}) edited the post {post_id}")

        
        db.session.commit()

        flash("Post updated successfully", "success")
        return redirect(url_for("user.see_post", post_id = post_to_edit.id))
    
    if request.method == "GET":
        form.title.data = post_to_edit.title
        form.body.data = post_to_edit.body

    return render_template("edit_post.html", form = form, post = post_to_edit)

@user_bp.route("/delete_post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)

    if post_to_delete.user_id != current_user.id and not current_user.is_admin:
        flash("You do not have permission to delete this post.", "danger")
        current_app.logger.warning(f"User {current_user.username} (ID:{current_user.id}) tried to delete {post_to_delete.author}'s post (ID:{post_id}) without permission")
        return redirect(url_for("user.see_all_posts"))

    db.session.delete(post_to_delete)
    db.session.commit()

    current_app.logger.warning(f"{current_user.username} (ID:{current_user.id}) has deleted post {post_id}")
    flash("Post deleted successfully!", "success")
    return redirect(url_for("user.see_all_posts"))
    
@user_bp.route("/like_post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def like_post(post_id):

    post = Post.query.get_or_404(post_id)

    check_like = Likes.query.filter_by(user_id = current_user.id, post_id = post_id).first()

    if check_like:
        db.session.delete(check_like)
        db.session.commit()

        current_app.logger.info(f"{current_user.username} (ID:{current_user.id}) has unliked {post.author.username}'s post (post ID:{post_id})")

        return redirect(url_for("user.see_all_posts"))

    like = Likes(
        user_id = current_user.id,
        post_id = post.id
    )

    db.session.add(like)
    db.session.commit()

    current_app.logger.info(f"{current_user.username} (ID:{current_user.id}) has liked {post.author.username}'s post {post_id}") 

    return redirect(url_for("user.see_all_posts"))


@user_bp.route("/like_comment/<int:comment_id>", methods=['GET', 'POST'])
@login_required
def like_post(comment_id):
    pass