"""Blueprint for user routes."""
import os
from flask import Blueprint
from flask_login import login_required, current_user
from src import db
from src.utils.user_utils import UserUtils
from src.utils.relationship_utils import RelationshipUtils
from src.models import Users, Relationship
from src.utils.forms import UserForm, LoginForm, SearchForm

template_folder = os.path.join("templates", "user")
static_folder = os.path.join("static", "user")
images_dir = os.path.join("src", static_folder, "images")
users = Blueprint('users', __name__, 
                  template_folder=template_folder,
                  static_folder=static_folder)
relationship_utils = RelationshipUtils(db,
                                        Users,
                                        Relationship)
user_utils = UserUtils(db, 
                       Users,
                       images_dir)




@users.route("/home")
@login_required
def user_home():
    """User page"""
    return user_utils.user_home()

@users.route("/<int:id>")
@login_required
def user(id):
    """User page"""
    if_friends = relationship_utils.check_if_friends(id, current_user._id)
    return user_utils.user(id, if_friends)

@users.route("/search", methods=["POST"])
@login_required
def search_user():
    """Search user in db"""
    form = SearchForm()
    return user_utils.search_user(form)

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

@users.route("/friends")
@login_required
def friends():
    """Friends page"""
    return relationship_utils.friends(current_user._id)

@users.route("/add_friend/<int:id>")
@login_required
def add_friend(id):
    """Add friend to db"""
    return relationship_utils.add_relationship(id, current_user._id)

@users.route("/accept_friend/<int:id>")
@login_required
def accept_friend(id):
    """Accept friend to db"""
    return relationship_utils.accept_relationship(id)

@users.route("/reject_friend/<int:id>")
@login_required
def reject_friend(id):
    """Reject friend to db"""
    return relationship_utils.reject_relationship(id)

@users.route("/remove_friend/<int:id>")
@login_required
def remove_friend(id):
    """Remove friend from db"""
    return relationship_utils.remove_relationship(id)

@users.route("/logout")
@login_required
def logout():
    """Logout page"""
    return user_utils.logout()
