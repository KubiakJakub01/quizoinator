"""Main app file"""
# Import flask and template operators
from flask import render_template

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
from src.models import Users, Admin
# Import forms
from src.utils.forms import SearchForm
# Import utils
from src.users import users
from src.blog import blog
from src.admin import admin


@login_menager.user_loader
def load_user(user_id):
    """Load user from database"""
    return Users.query.get(int(user_id))


@app.context_processor
def base():
    """Base context for all templates"""
    form = SearchForm()
    admin_list = Admin.query.all()
    return dict(form=form, admin_list=admin_list)


@app.route("/")
def home():
    """Home page"""
    return render_template("base/index.html")


if __name__ == "__main__":
    app = create_app(app)
    db = init_db(app)
    login_menager = init_login_manager(app)
    ckeditor = init_ckeditor(app)

    app.register_blueprint(users, url_prefix="/user")
    app.register_blueprint(blog, url_prefix="/blog")
    app.register_blueprint(admin, url_prefix="/admin")

    with app.app_context():
        db.create_all()
    app.run(debug=True)
