from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_login import current_user, login_required
from extensions import db
from models import Post

post_bp = Blueprint("post", __name__, url_prefix="/posts")

@post_bp.route("/list_posts")
@login_required
def list_posts():
    current_app.logger.info(f"User {current_user.username} accessed the posts list page.")
    all_posts = db.session.execute(db.select(Post)).scalars().all()
    return render_template("list_posts.html", posts=all_posts)