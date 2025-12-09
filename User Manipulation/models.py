from extensions import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Boolean, Text, Table, Column, CheckConstraint
from datetime import datetime, timezone
from typing import List

class User(UserMixin, db.Model):
    __tablename__ = "users"


    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    username: Mapped[str] = mapped_column(String(50), unique = True, nullable = False)
    email: Mapped[str] = mapped_column(String(120), unique = True, nullable = False)
    password: Mapped[str] = mapped_column(String(200), nullable = False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default = False)
    profile_pic: Mapped[str] = mapped_column(String(250), nullable = True, default = "default.png")

    posts = relationship("Post", back_populates = "author", cascade = "all, delete-orphan")

    likes: Mapped[List["Likes"]] = relationship("Likes", back_populates = "author", cascade = "all, delete-orphan")
    comments: Mapped[List["Comments"]] = relationship("Comments", back_populates = "author", cascade = "all, delete-orphan")
    shared: Mapped[List["Shared"]] = relationship("Shared", back_populates = "author", cascade = "all, delete-orphan")



class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    title: Mapped[str] = mapped_column(String(200), nullable = False)
    body: Mapped[str] = mapped_column(Text, nullable = False)
    date = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    post_pic: Mapped[str] = mapped_column(String(250), nullable = True)

    author = relationship("User", back_populates = "posts")

    likes: Mapped[List["Likes"]] = relationship("Likes", back_populates = "post", cascade = "all, delete-orphan")
    comments: Mapped[List["Comments"]] = relationship("Comments", back_populates = "post", cascade = "all, delete-orphan")
    shared: Mapped[List["Shared"]] = relationship("Shared", back_populates = "post", cascade = "all, delete-orphan")

class Likes(db.Model):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete = "CASCADE"), nullable = True)
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id", ondelete = "CASCADE"), nullable = True)
    shared_id: Mapped[int] = mapped_column(ForeignKey("shared.id", ondelete = "CASCADE"), nullable = True)

    __table_args__ = (
        CheckConstraint("(post_id IS NOT NULL AND comment_id IS NULL AND shared_id IS NULL) OR " "(post_id IS NULL AND comment_id IS NOT NULL AND shared_id IS NULL) OR " "(post_id IS NULL AND comment_id IS NULL AND shared_id IS NOT NULL)",
            name = "only_one_like_target"
        ),
    )

    author = relationship("User", back_populates = "likes")
    post = relationship("Post", back_populates = "likes")
    comment = relationship("Comments", back_populates = "likes")
    shared = relationship("Shared", back_populates = "likes")

    
class Comments(db.Model):
    __tablename__ = "comments"

    id = mapped_column(Integer, primary_key = True)
    user_id = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    post_id = mapped_column(ForeignKey("posts.id", ondelete = "CASCADE"), nullable = True)
    shared_id = mapped_column(ForeignKey("shared.id", ondelete = "CASCADE"), nullable = True)
    body = mapped_column(Text, nullable = False)
    date = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

    likes = relationship("Likes", back_populates = "comment", cascade = "all, delete-orphan")

    __table_args__ = (
        CheckConstraint(
            "(post_id IS NOT NULL AND shared_id IS NULL) OR "
            "(post_id IS NULL AND shared_id IS NOT NULL)",
            name = "comment_target_check"
        ),
    )

    author = relationship("User", back_populates = "comments")
    post = relationship("Post", back_populates = "comments", foreign_keys = [post_id])
    shared = relationship("Shared", back_populates = "comments", foreign_keys = [shared_id])

class Shared(db.Model):
    __tablename__ = "shared"

    id: Mapped[int] = mapped_column(Integer, primary_key =  True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete = "CASCADE"), nullable = False)
    shared_id: Mapped[int] = mapped_column(ForeignKey("shared.id", ondelete="CASCADE"), nullable = True)
    body: Mapped[str] = mapped_column(Text, nullable = True)
    date = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))

    likes: Mapped[List["Likes"]] = relationship("Likes", back_populates = "shared", cascade = "all, delete-orphan")
    parent_shared = relationship("Shared", remote_side = [id], backref = "children")

    author = relationship("User", back_populates = "shared")
    post = relationship("Post", back_populates = "shared")
    comments = relationship("Comments", back_populates = "shared")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))