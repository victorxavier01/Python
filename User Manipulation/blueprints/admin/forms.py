from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from flask_wtf.file import FileField, FileAllowed


class EditForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50), Regexp("^[a-zA-Z0-9_]+$", message="Use apenas letras, números e _")])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password")
    profile_pic = FileField("Profile Picture", validators=[FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField("Edit")