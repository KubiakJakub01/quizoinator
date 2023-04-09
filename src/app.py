"""Main app file"""
from datetime import timedelta

# Import flask and template operators
from flask import Flask, redirect, url_for, render_template, session, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_ckeditor import CKEditor

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey

# Import password / encryption helper tools
from werkzeug.security import generate_password_hash, check_password_hash

# Import forms
from utils.forms import UserForm, LoginForm, PostForm, SearchForm, AdminForm
from utils.posts_utils import PostsUtils
from utils.user_utils import UserUtils
from utils.admin_utils import AdminUtils

# Define the application configuration
app = Flask(__name__)
ckeditor = CKEditor(app)
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

@app.context_processor
def base():
    """Base context for all templates"""
    form = SearchForm()
    admin_list = admin_utils.get_admins
    return dict(form=form, admin_list=admin_list)


@app.route("/")
def home():
    """Home page"""
    return render_template("base/index.html")


@app.route("/user")
@login_required
def user():
    """User page"""
    return render_template("user/user.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Sign up page"""
    form = UserForm()
    return user_utils.add_user(form)


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
    return render_template("user/login.html", form=form)


@app.route("/update/<int:id>", methods=["POST", "GET"])
@login_required
def update(id):
    """Update user in db"""
    form = UserForm()
    return user_utils.update_user(id, form)


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    """Delete user from db"""
    return user_utils.delete_user(id)

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
    return posts_utils.add_post(form, author_id=current_user._id)

@app.route("/post/view")
@login_required
def view_posts():
    """View all posts in db"""
    return posts_utils.view_posts()

@app.route("/post/view/<int:id>")
@login_required
def view_post(id):
    """View single post in db"""
    return posts_utils.view_post(id)

@app.route("/post/update/<int:id>", methods=["POST", "GET"])
@login_required
def update_post(id):
    """Update post in db"""
    form = PostForm()
    return posts_utils.update_post(id, form, author_id=current_user._id)

@app.route("/post/delete/<int:id>")
@login_required
def delete_post(id):
    """Delete post from db"""
    return posts_utils.delete_post(id, author_id=current_user._id)

@app.route("/post/search", methods=["POST"])
@login_required
def search_post():
    """Search post in db"""
    form = SearchForm()
    return posts_utils.search_post(form)

@app.route("/admin")
@login_required
def admin():
    """Admin page"""
    id = current_user._id
    return admin_utils.admin(id)

@app.route("/admin/view")
@login_required
def view():
    """View all user in db"""
    id = current_user._id
    return admin_utils.view_users(id)

@app.route("/admin/add_admin", methods=["POST", "GET"])
@login_required
def add_admin():
    """Add admin to db"""
    id = current_user._id
    form = AdminForm()
    return admin_utils.add_admin(id, form)

class Users(db.Model, UserMixin):
    """User model for sqlalchemy database"""

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    email = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(128))
    data_created = Column(db.DateTime, default=db.func.current_timestamp())
    posts = db.relationship("Posts", backref="author", lazy=True)

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
        return self.name


class Posts(db.Model):
    """Posts model for sqlalchemy database"""

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, unique=True)
    content = Column(Text, nullable=False, unique=True)
    data_created = Column(db.DateTime, default=db.func.current_timestamp())
    # Foreign key to Users
    author_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return f"Post {self.title} with content {self.content}"


class Admin(db.Model):
    """Admin model for sqlalchemy database"""

    admin_id = Column("id", Integer, primary_key=True, autoincrement=True)
    # Foreign key to Users
    user_id = Column(Integer, ForeignKey("users.id"))
    # Foreign key to person who added admin
    added_by = Column(Integer, ForeignKey("users.id"))
    # reason for adding admin
    reason = Column(String(200), nullable=False)
    # Date admin was added
    date_added = Column(db.DateTime, default=db.func.current_timestamp())



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    admin_utils = AdminUtils(db, Admin,  Users, Posts, "admin")
    user_utils = UserUtils(db, Users, "user")
    posts_utils = PostsUtils(db, Posts, "blog")
    app.run(debug=True)
