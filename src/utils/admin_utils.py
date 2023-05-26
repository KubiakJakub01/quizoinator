"""
Module for admin utilities
"""
from flask import render_template, redirect, url_for, flash


class AdminUtils:
    """Admin utils"""

    def __init__(self, db, Admin, User, Posts):
        self.db = db
        self.Admin = Admin
        self.User = User
        self.Posts = Posts

    @property
    def get_admins(self):
        """Get admins"""
        return [admin.user_id for admin in self.Admin.query.all()]

    def verify_admin(self, id):
        """Verify admin"""
        if id in self.get_admins:
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
                return redirect(url_for("user.home"))

        return wrapper

    @_admin_required
    def view_users(self, id):
        """View users"""
        users = self.User.query.all()
        return render_template("view.html", users=users)

    @_admin_required
    def admin(self, id):
        """Admin"""
        return render_template("admin.html")

    @_admin_required
    def add_admin(self, id, form):
        """Add admin"""
        users = self.User.query.all()
        if form.validate_on_submit():
            if self.Admin.query.filter_by(user_id=form.user_id.data).first():
                flash("Admin already exists!", "error")
                return redirect(url_for("admin.admin_home"))
            else:
                admin = self.Admin(
                    user_id=form.user_id.data, added_by=id, reason=form.reason.data
                )
                form.user_id.data = ""
                form.reason.data = ""
                self.db.session.add(admin)
                self.db.session.commit()
                self.admin_list.append(admin.user_id)
                flash("Admin added!", "info")
                return redirect(url_for("admin.admin_home"))
        return render_template("add_admin.html", form=form, users=users)

    @_admin_required
    def view_admins(self, id):
        """View admins"""
        admins = self.Admin.query.all()
        return render_template("view_admins.html", admins=admins)

    @_admin_required
    def delete_user(self, id, user_id):
        """Delete user"""
        user_to_delete = self.User.query.get_or_404(user_id)
        if user_to_delete._id in self.admin_list:
            flash("You cannot delete an admin!", "error")
            return redirect(url_for("admin.view_users"))
        try:
            self.db.session.delete(user_to_delete)
            self.db.session.commit()
            flash("User deleted!", "info")
            return redirect(url_for("admin.view_users"))
        except:
            flash("There was an issue deleting your user", "error")
            return redirect(url_for("admin.view_users"))

    @_admin_required
    def delete_post(self, id, post_id):
        """Delete post"""
        post_to_delete = self.Posts.query.get_or_404(post_id)
        try:
            self.db.session.delete(post_to_delete)
            self.db.session.commit()
            flash("Post deleted!", "info")
            return redirect(url_for("admin.view_posts"))
        except:
            flash("There was an issue deleting your post", "error")
            return redirect(url_for("admin.view_posts"))
