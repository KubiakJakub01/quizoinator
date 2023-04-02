from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = "mysecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

login_menager = LoginManager()
login_menager.init_app(app)
login_menager.login_view = "login"

@login_menager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    email = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(128))
    data_created = Column(db.DateTime, default=db.func.current_timestamp())

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self._id

    def __repr__(self):
        return f"User {self.name} with email {self.email}"


class UserForm(FlaskForm):
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
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/user")
@login_required
def user():
    return render_template("user.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    name = None
    email = None
    password = None
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        found_user = Users.query.filter_by(name=name).first()
        if found_user:
            flash("User already exists!")
            return redirect(url_for("login"))
        else:
            usr = Users(name=name, email=email, password=password)
            db.session.add(usr)
            db.session.commit()
            flash("User created!")
            return redirect(url_for("login"))
    return render_template(
        "signup.html", form=form
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    name = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        found_user = Users.query.filter_by(name=name).first()
        if found_user:
            if found_user.verify_password(password):
                login_user(found_user)
                session.permanent = True
                session["user"] = name
                flash("Logged in successfully!", "info")
                return redirect(url_for("user"))
            else:
                flash("Invalid credentials!", "error")
                return redirect(url_for("login"))
        flash("This user doesn't exist!", "error")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/view")
def view():
    return render_template("view.html", users=Users.query.all())


@app.route("/logout")
@login_required
def logout():
    flash(f"You have been logged out", "info")
    logout_user()
    return redirect(url_for("home"))


@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
