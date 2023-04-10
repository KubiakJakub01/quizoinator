"""Blueprint for user routes."""
import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, login_required, current_user
from src import db
from src.utils.user_utils import UserUtils
from src.models import Users
from src.utils.forms import UserForm, LoginForm

users = Blueprint('users', __name__, 
                  template_folder=os.path.join('templates', 'user'))
user_utils = UserUtils(db, Users)

@users.route("/home")
@login_required
def user_home():
    """User page"""
    return user_utils.user_home()

@users.route("/<int:id>")
@login_required
def user(id):
    """User page"""
    return user_utils.user(id)

@users.route("/signup", methods=["POST", "GET"])
def signup():
    """Sign up page"""
    form = UserForm()
    return user_utils.add_user(form)

@users.route("/login", methods=["POST", "GET"])
def login():
    """Login page"""
    form = LoginForm()
    return user_utils.login(form)

@users.route("/update/<int:id>", methods=["POST", "GET"])
@login_required
def update(id):
    """Update user in db"""
    form = UserForm()
    return user_utils.update_user(id, form)

@users.route("/delete/<int:id>")
@login_required
def delete(id):
    """Delete user from db"""
    return user_utils.delete_user(id)


@users.route("/logout")
@login_required
def logout():
    """Logout page"""
    return user_utils.logout()
