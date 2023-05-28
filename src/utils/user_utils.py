"""
Module for user related functions
"""
import os
import uuid
from pathlib import Path
from flask import flash, redirect, render_template, url_for, request, session
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename


class UserUtils:
    """Class for user related functions"""

    def __init__(self, db, Users, images_dir):
        self.db = db
        self.Users = Users
        self.images_dir = Path(images_dir)
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def user_home(self):
        """User home page"""
        return render_template("user_home.html")

    def user(self, id):
        """User profile"""
        user = self.Users.query.filter_by(_id=id).first()
        return render_template("user.html", user=user)

    def login(self, form):
            """Login page"""
            if form.validate_on_submit():
                name = form.name.data
                password = form.password.data
                found_user = self.Users.query.filter_by(name=name).first()
                if found_user:
                    if found_user.verify_password(password):
                        login_user(found_user)
                        session.permanent = True
                        session["user"] = name
                        flash("Logged in successfully!", "info")
                        return redirect(url_for("users.user_home"))
                    else:
                        flash("Invalid credentials!", "error")
                        return redirect(url_for("users.login"))
                flash("This user doesn't exist!", "error")
                return redirect(url_for("users.login"))
            return render_template("login.html", form=form)

    def logout(self):
        """Logout page"""
        logout_user()
        session.clear()
        flash("Logged out successfully!", "info")
        return redirect(url_for("users.login"))

    def process_picture(self, picture):
        """Process picture"""
        if not picture:
            pic_name = "default.png"
        else:
            profile_filename = secure_filename(picture.filename)
            pic_name = str(uuid.uuid4()) + profile_filename
            picture.save(str(self.images_dir / pic_name))
        return pic_name

    def add_user(self, form):
        """Sign up page"""
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            profile_picture = form.profile_picture.data
            pic_name = self.process_picture(profile_picture)
            found_user = self.Users.query.filter_by(name=name).first()
            form.name.data = ""
            form.email.data = ""
            form.password.data = ""
            form.profile_picture.data = ""
            if found_user:
                flash("User already exists!")
                return redirect(url_for("users.login"))
            else:
                usr = self.Users(name=name, email=email, password=password, profile_picture=pic_name)
                self.db.session.add(usr)
                self.db.session.commit()
                flash("User created!")
                return redirect(url_for("users.login"))
        return render_template("signup.html", form=form)

    def update_user(self, id, form):
        """Update user in db"""
        name_to_update = self.Users.query.get_or_404(id)
        if request.method == "POST":
            name_to_update.name = form.name.data
            name_to_update.email = form.email.data
            profile_picture = form.profile_picture.data
            name_to_update.profile_picture = self.process_picture(profile_picture) 
            try:
                self.db.session.commit()
                flash("User updated!", "info")
                return render_template("user_home.html")
            except:
                flash("There was an issue updating your task", "error")
                return render_template(
                    "update.html",
                    form=form,
                    name_to_update=name_to_update,
                )
        else:
            form.name.data = name_to_update.name
            form.email.data = name_to_update.email
            form.profile_picture.data = name_to_update.profile_picture
            return render_template(
                "update.html",
                form=form,
                name_to_update=name_to_update,
                id=id,
            )

    def delete_user(self, id):
        """Delete user from db"""
        name_to_delete = self.Users.query.get_or_404(id)
        if current_user._id == name_to_delete._id:
            try:
                self.db.session.delete(name_to_delete)
                self.db.session.commit()
                flash("User deleted!", "info")
                return redirect(url_for("home"))
            except:
                flash("There was an issue deleting your task", "error")
                return redirect(url_for("users.user_home"))
        else:
            flash("You can't delete this profile!", "error")
            return redirect(url_for("users.user_home"))

    def get_user(self, name):
        """Get user from db"""
        user = self.Users.query.filter_by(name=name).first()
        return user

    def get_users(self):
        """Get all users from db"""
        users = self.Users.query.all()
        return users
