"""Main app file"""
from datetime import timedelta

# Import flask and template operators
from flask import Flask, redirect, url_for, render_template, session, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text

# Import password / encryption helper tools
from werkzeug.security import generate_password_hash, check_password_hash

# Import forms
from utils.forms import UserForm, LoginForm, PostForm
from utils.posts_utils import PostsUtils

# Define the application configuration
app = Flask(__name__)
app.secret_key = "mysecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

# Define the database object which is imported
db = SQLAlchemy(app)

# Define login manager
login_menager = LoginManager()
login_menager.init_app(app)
login_menager.login_view = "login"


@login_menager.user_loader
def load_user(user_id):
    """Load user from database"""
    return Users.query.get(int(user_id))


@app.route("/")
def home():
    """Home page"""
    return render_template("index.html")


@app.route("/user")
@login_required
def user():
    """User page"""
    return render_template("user.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Sign up page"""
    name = None
    email = None
    password = None
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        found_user = Users.query.filter_by(name=name).first()
        form.name.data = ""
        form.email.data = ""
        form.password.data = ""
        if found_user:
            flash("User already exists!")
            return redirect(url_for("login"))
        else:
            usr = Users(name=name, email=email, password=password)
            db.session.add(usr)
            db.session.commit()
            flash("User created!")
            return redirect(url_for("login"))
    return render_template("signup.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    """Login page"""
    name = None
    password = None
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        found_user = Users.query.filter_by(name=name).first()
        if found_user:
            if found_user.verify_password(password):
                login_user(found_user)
                session.permanent = True
                session["user"] = name
                flash("Logged in successfully!", "info")
                return redirect(url_for("user"))
            else:
                flash("Invalid credentials!", "error")
                return redirect(url_for("login"))
        flash("This user doesn't exist!", "error")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route("/update/<int:id>", methods=["POST", "GET"])
@login_required
def update(id):
    """Update user in db"""
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = form.name.data
        name_to_update.email = form.email.data
        try:
            db.session.commit()
            flash("User updated!", "info")
            return render_template("user.html")
        except:
            flash("There was an issue updating your task", "error")
            return render_template("update.html", 
                                   form=form,
                                   name_to_update=name_to_update)
    else:
        form.name.data = name_to_update.name
        form.email.data = name_to_update.email
        return render_template("update.html", 
                               form=form,
                               name_to_update=name_to_update,
                               id=id)


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    """Delete user from db"""
    name_to_delete = Users.query.get_or_404(id)
    id = current_user._id
    if id == name_to_delete._id:
        try:
            db.session.delete(name_to_delete)
            db.session.commit()
            flash("User deleted!", "info")
            return redirect(url_for("user"))
        except:
            flash("There was an issue deleting your task", "error")
            return redirect(url_for("user"))
    else:
        flash("You can't delete this profile!", "error")
        return redirect(url_for("user"))


@app.route("/logout")
@login_required
def logout():
    """Logout page"""
    flash(f"You have been logged out", "info")
    logout_user()
    return redirect(url_for("home"))


@app.route("/post/add", methods=["POST", "GET"])
@login_required
def add_post():
    """Add post to db"""
    form = PostForm()
    return posts_utils.add_post(form, author=current_user.name)

@app.route("/post/view")
@login_required
def view_posts():
    """View all posts in db"""
    return posts_utils.view_posts()

@app.route("/post/view/<int:id>", methods=["POST", "GET"])
@login_required
def view_post(id):
    """View single post in db"""
    return posts_utils.view_post(id)


@app.route("/admin")
def admin():
    """Admin page"""
    return redirect(url_for("user", name="Admin!"))


@app.route("/view")
def view():
    """View all user in db"""
    return render_template("view.html", users=Users.query.all())


class Users(db.Model, UserMixin):
    """User model for sqlalchemy database"""

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    email = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(128))
    data_created = Column(db.DateTime, default=db.func.current_timestamp())

    @property
    def password(self):
        """Prevent password from being accessed"""
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Set password to a hashed password"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check if hashed password matches actual password"""
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Return id"""
        return self._id

    def __repr__(self):
        return f"User {self.name} with email {self.email}"


class Posts(db.Model):
    """Posts model for sqlalchemy database"""

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, unique=True)
    content = Column(Text, nullable=False, unique=True)
    author = Column(String(20), nullable=False)
    data_created = Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"Post {self.title} with content {self.content}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    posts_utils = PostsUtils(db, Posts)
    app.run(debug=True)
