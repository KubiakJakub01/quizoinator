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


@app.route("/post/like/<int:id>")
@login_required
def like_post(id):
    """Like post"""
    return posts_utils.like_post(id, current_user._id)


@app.route("/post/who_liked/<int:id>")
@login_required
def who_liked(id):
    """Who liked post"""
    return posts_utils.view_who_liked_post(id)

@app.route("/post/comment/<int:id>", methods=["POST"])
@login_required
def add_comment(id):
    """Add comment to post"""
    form = CommentForm()
    return comment_utils.add_comment(id, form, current_user._id)


@app.route("/post/comment/delete/<int:id>")
@login_required
def delete_comment(id):
    """Delete comment from post"""
    return comment_utils.delete_comment(id, current_user._id)

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

    with app.app_context():
        db.create_all()
        admin_utils = AdminUtils(db, Admin, Users, Posts, "admin")
    # user_utils = UserUtils(db, Users, "user")
    comment_utils = CommentsUtils(db, Comments, "blog")
    posts_utils = PostsUtils(db, Posts, PostsLikes, "blog")
    app.run(debug=True)
