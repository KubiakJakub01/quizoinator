from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "mysecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class User(db.Model):
    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100))
    password_hash = Column(String(128))
    
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
            found_user = User.query.filter_by(name=user_name).first()
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
    pass

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        name = request.form["name"]
        session["user"] = name
        email = request.form["email"]
        session["email"] = email
        flash("Login Successful!")
        found_user = User.query.filter_by(name=name).first()
        if found_user:
            flash("User already exists!")
            session["email"] = found_user.email
        else:
            usr = User(name=name, email=email)
            db.session.add(usr)
            db.session.commit()
            flash("User created!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")


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
