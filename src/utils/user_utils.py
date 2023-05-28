"""
Module for user related functions
"""
from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user


class UserUtils:
    """Class for user related functions"""

    def __init__(self, db, Users):
        self.db = db
        self.Users = Users

    def add_user(self, form):
        """Sign up page"""
        name = None
        email = None
        password = None
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            found_user = self.Users.query.filter_by(name=name).first()
            form.name.data = ""
            form.email.data = ""
            form.password.data = ""
            if found_user:
                flash("User already exists!")
                return redirect(url_for("login"))
            else:
                usr = self.Users(name=name, email=email, password=password)
                self.db.session.add(usr)
                self.db.session.commit()
                flash("User created!")
                return redirect(url_for("login"))
        return render_template("signup.html", form=form)

    def update_user(self, id, form):
        """Update user in db"""
        name_to_update = self.Users.query.get_or_404(id)
        if request.method == "POST":
            name_to_update.name = form.name.data
            name_to_update.email = form.email.data
            try:
                self.db.session.commit()
                flash("User updated!", "info")
                return render_template("user.html")
            except:
                flash("There was an issue updating your task", "error")
                return render_template(
                    "update.html", form=form, name_to_update=name_to_update
                )
        else:
            form.name.data = name_to_update.name
            form.email.data = name_to_update.email
            return render_template(
                "update.html", form=form, name_to_update=name_to_update, id=id
            )

    def delete_user(self, id):
        """Delete user from db"""
        name_to_delete = self.Users.query.get_or_404(id)
        id = current_user._id
        if id == name_to_delete._id:
            try:
                self.db.session.delete(name_to_delete)
                self.db.session.commit()
                flash("User deleted!", "info")
                return redirect(url_for("user"))
            except:
                flash("There was an issue deleting your task", "error")
                return redirect(url_for("user"))
        else:
            flash("You can't delete this profile!", "error")
            return redirect(url_for("user"))

    def get_user(self, name):
        """Get user from db"""
        user = self.Users.query.filter_by(name=name).first()
        return user

    def get_users(self):
        """Get all users from db"""
        users = self.Users.query.all()
        return users
