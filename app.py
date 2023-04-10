"""Main app file"""
# Import flask and template operators
from flask import redirect, url_for, render_template, session, flash
from flask_login import login_user, login_required, logout_user, current_user

# Import init
from src import (
    app,
    db,
    login_menager,
    create_app,
    init_db,
    init_login_manager,
    init_ckeditor,
)

# Import models
from src.models import Users, Posts, Admin

# Import utils
from src.utils.forms import UserForm, LoginForm, PostForm, SearchForm, AdminForm
from src.utils.posts_utils import PostsUtils
from src.utils.user_utils import UserUtils
from src.utils.admin_utils import AdminUtils


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
def view_users():
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


@app.route("/admin/view_admin")
@login_required
def view_admins():
    """View all admins in db"""
    id = current_user._id
    return admin_utils.view_admins(id)

@app.route("/admin/delete_user/<int:id>")
@login_required
def admin_delete_user(id):
    """Delete user from db"""
    current_user_id = current_user._id
    return admin_utils.delete_user(current_user_id, id)


if __name__ == "__main__":
    app = create_app(app)
    db = init_db(app)
    login_menager = init_login_manager(app)
    ckeditor = init_ckeditor(app)

    with app.app_context():
        db.create_all()
        admin_utils = AdminUtils(db, Admin, Users, Posts, "admin")
    user_utils = UserUtils(db, Users, "user")
    posts_utils = PostsUtils(db, Posts, "blog")
    app.run(debug=True)
