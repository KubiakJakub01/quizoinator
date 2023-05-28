"""Initialize Flask app."""
from datetime import timedelta

# Import flask and template operators
from flask import Flask
from flask_ckeditor import CKEditor

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy()
login_menager = LoginManager()


def create_app(app):
    app.secret_key = "mysecret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.permanent_session_lifetime = timedelta(minutes=5)
    return app


def init_db(app):
    db.init_app(app)
    return db


def init_login_manager(app):
    login_menager.init_app(app)
    login_menager.login_view = "login"
    return login_menager


def init_ckeditor(app):
    ckeditor = CKEditor(app)
    return ckeditor
