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
from wtforms.validators import DataRequired, Email, EqualTo, Length

app = Flask(__name__)
app.secret_key = "mysecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class Users(db.Model):
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

    def __repr__(self):
        return f"User {self.name} with email {self.email}"

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("password2", message="Passwords must match")])
    password2 = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/user")
def user():
    email = None
    if "user" in session:
        user_name = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = Users.query.filter_by(name=user_name).first()
            found_user.email = email
            db.session.commit()
        else:
            if "email" in session:
                email = session["email"]
        return render_template(
            "user.html", name=user_name, email=email, content=["HTML", "CSS", "JS"]
        )
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))


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
    return render_template("signup.html",
                            name=name,
                            email=email,
                            password=password,
                            form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        name = request.form["name"]
        session["user"] = name
        email = request.form["email"]
        session["email"] = email
        flash("Login Successful!")
        found_user = Users.query.filter_by(name=name).first()
        if found_user:
            flash("User already exists!")
            session["email"] = found_user.email
        else:
            usr = Users(name=name, email=email)
            db.session.add(usr)
            db.session.commit()
            flash("User created!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/view")
def view():
    return render_template("view.html", users=Users.query.all())


@app.route("/logout")
def logout():
    flash(f"You have been logged out", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
