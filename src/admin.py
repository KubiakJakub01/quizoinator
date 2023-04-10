"""Blueprint for admin routes."""
import os
from flask import Blueprint
from flask_login import login_required, current_user
from src import db
from src.utils.admin_utils import AdminUtils
from src.models import Admin, Users, Posts
from src.utils.forms import AdminForm

admin = Blueprint('admin', __name__,
                    template_folder=os.path.join('templates', 'admin'))
admin_utils = AdminUtils(db, Admin, Users, Posts)


@admin.route("/")
@login_required
def admin_home():
    """Admin page"""
    return admin_utils.admin(current_user._id)


@admin.route("/view")
@login_required
def view_users():
    """View all user in db"""
    return admin_utils.view_users(current_user._id)


@admin.route("/add_admin", methods=["POST", "GET"])
@login_required
def add_admin():
    """Add admin to db"""
    id = current_user._id
    form = AdminForm()
    return admin_utils.add_admin(id, form)


@admin.route("/view_admin")
@login_required
def view_admins():
    """View all admins in db"""
    id = current_user._id
    return admin_utils.view_admins(id)

@admin.route("/delete_user/<int:id>")
@login_required
def admin_delete_user(id):
    """Delete user from db"""
    current_user_id = current_user._id
    return admin_utils.delete_user(current_user_id, id)


@admin.route("/delete_post/<int:id>")
@login_required
def admin_delete_post(id):
    """Delete post from db"""
    current_user_id = current_user._id
    return admin_utils.delete_post(current_user_id, id)
