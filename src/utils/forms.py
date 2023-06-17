"""
Module for forms
"""
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    FileField,
    TextAreaField,
    IntegerField,
    FieldList,
    BooleanField,
    FormField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length
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


class QuizForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[Length(max=500)])
    num_questions = IntegerField("Number of Questions", validators=[DataRequired()])
    questions = FieldList(
        TextAreaField("Questions", validators=[DataRequired(), Length(max=4)])
    )
    answers = FieldList(
        TextAreaField("Answers", validators=[DataRequired(), Length(max=4)])
    )
    submit = SubmitField("Create Quiz")


class AnswerForm(FlaskForm):
    text = StringField("Answer", validators=[DataRequired(), Length(max=100)])
    is_correct = BooleanField("Correct?")
    submit = SubmitField("Add Answer Form")


class QuestionForm(FlaskForm):
    question_text = TextAreaField(
        "Question", validators=[DataRequired(), Length(max=500)]
    )
    answers = FieldList(FormField(AnswerForm), min_entries=1, max_entries=4)
    submit = SubmitField("Add QuestionForm")


class QuizView(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[Length(max=500)])
