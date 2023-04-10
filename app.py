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
from src.models import Users, Posts, Admin, Comments, PostsLikes

# Import utils
from src.utils.forms import UserForm, LoginForm, PostForm, SearchForm, AdminForm, CommentForm
from src.utils.posts_utils import PostsUtils
from src.utils.user_utils import UserUtils
from src.utils.admin_utils import AdminUtils
from src.utils.comments_utils import CommentsUtils
from src.users import users
from src.blog import blog


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


@app.route("/admin")
@login_required
def admin():
    """Admin page"""
    return admin_utils.admin(current_user._id)


@app.route("/admin/view")
@login_required
def view_users():
    """View all user in db"""
    return admin_utils.view_users(current_user._id)


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


@app.route("/admin/delete_post/<int:id>")
@login_required
def admin_delete_post(id):
    """Delete post from db"""
    current_user_id = current_user._id
    return admin_utils.delete_post(current_user_id, id)


if __name__ == "__main__":
    app = create_app(app)
    db = init_db(app)
    login_menager = init_login_manager(app)
    ckeditor = init_ckeditor(app)

    app.register_blueprint(users, url_prefix="/user")
    app.register_blueprint(blog, url_prefix="/blog")

    with app.app_context():
        db.create_all()
        admin_utils = AdminUtils(db, Admin, Users, Posts, "admin")
    app.run(debug=True)
