from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50), Regexp("^[a-zA-Z0-9_]+$", message="Use apenas letras, números e _")])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    profile_pic = FileField("Profile Picture", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Login")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = CKEditorField("Body", validators=[DataRequired()])
    post_pic = FileField("Imagem do Post", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Send Post")

class EditPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = CKEditorField("Body", validators=[DataRequired()])
    post_pic = FileField("Imagem do Post", validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Confirm Edit")

class CommentForm(FlaskForm):
    body = TextAreaField("What do you think?", validators=[DataRequired()])
    post_id = HiddenField("Post ID", validators=[DataRequired()])
    submit = SubmitField("Comment")
