"""
Module for admin utilities
"""
from pathlib import Path
from flask import render_template, redirect, url_for, flash

class AdminUtils:
    """Admin utils"""

    def __init__(self, db, Admin, User, Posts, admin_dir):
        self.db = db
        self.Admin = Admin
        self.User = User
        self.Posts = Posts
        # self.admin_list = [admin.id for admin in self.Admin.query.all()]
        self.admin_list = [1]
        self.admin_dir = Path(admin_dir)

    @property
    def get_admins(self):
        """Get admins"""
        return self.admin_list

    def verify_admin(self, id):
        """Verify admin"""
        if id in self.admin_list:
            return True
        else:
            return False

    def _admin_required(func):
        def wrapper(self, *args, **kwargs):
            id = args[0]
            if self.verify_admin(id):
                return func(self, *args, **kwargs)
            else:
                flash("You are not an admin!", "error")
                return redirect(url_for("home"))
        return wrapper

    @_admin_required
    def view_users(self, id):
        """View users"""
        users = self.User.query.all()
        return render_template(str(self.admin_dir / "view.html"), users=users)
    
    @_admin_required
    def admin(self, id):
        """Admin"""
        return render_template(str(self.admin_dir / "admin.html"))

    @_admin_required
    def add_admin(self, id, form):
        """Add admin"""
        users = self.User.query.all()
        if form.validate_on_submit():
            if self.Admin.query.filter_by(user_id=form.user_id.data).first():
                flash("Admin already exists!", "error")
                return redirect(url_for("admin"))
            else:
                admin = self.Admin(user_id=form.user_id.data,
                                   added_by=id,
                                   reason=form.reason.data)
                form.user_id.data = ""
                form.reason.data = ""
                self.db.session.add(admin)
                self.db.session.commit()
                flash("Admin added!", "info")
                return redirect(url_for("admin"))
        return render_template(str(self.admin_dir / "add_admin.html"), form=form, users=users)

