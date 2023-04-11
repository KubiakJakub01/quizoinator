"""
Module for forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField


class UserForm(FlaskForm):
    """User form for registration"""

    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Passwords must match"),
        ],
    )
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    profile_picture = FileField("Profile Picture")
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    """User form for login"""

    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class PostForm(FlaskForm):
    """Post form"""

    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    """Search form"""

    searched = StringField("Search", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AdminForm(FlaskForm):
    """Admin form"""

    user_id = StringField("User ID", validators=[DataRequired()])
    reason = StringField("Reason", widget=TextArea())
    submit = SubmitField("Submit")


class CommentForm(FlaskForm):
    """Comment form"""

    comment = StringField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")
