"""Blueprint for the post routes."""
import os
from flask import Blueprint
from flask_login import login_required, current_user
from src import db
from src.utils.posts_utils import PostsUtils
from src.utils.comments_utils import CommentsUtils
from src.models import Posts, Comments, PostsLikes
from src.utils.forms import PostForm, SearchForm, CommentForm

blog = Blueprint("blog", __name__, template_folder=os.path.join("templates", "blog"))
posts_utils = PostsUtils(db, Posts, PostsLikes)
comment_utils = CommentsUtils(db, Comments)


@blog.route("/add", methods=["POST", "GET"])
@login_required
def add_post():
    """Add post to db"""
    form = PostForm()
    return posts_utils.add_post(form, author_id=current_user._id)


@blog.route("/view")
@login_required
def view_posts():
    """View all posts in db"""
    return posts_utils.view_posts()


@blog.route("/view/<int:id>")
@login_required
def view_post(id):
    """View single post in db"""
    return posts_utils.view_post(id)


@blog.route("/update/<int:id>", methods=["POST", "GET"])
@login_required
def update_post(id):
    """Update post in db"""
    form = PostForm()
    return posts_utils.update_post(id, form, author_id=current_user._id)


@blog.route("/delete/<int:id>")
@login_required
def delete_post(id):
    """Delete post from db"""
    return posts_utils.delete_post(id, author_id=current_user._id)


@blog.route("/search", methods=["POST"])
@login_required
def search_post():
    """Search post in db"""
    form = SearchForm()
    return posts_utils.search_post(form)


@blog.route("/like/<int:id>")
@login_required
def like_post(id):
    """Like post"""
    return posts_utils.like_post(id, current_user._id)


@blog.route("/who_liked/<int:id>")
@login_required
def who_liked(id):
    """Who liked post"""
    return posts_utils.view_who_liked_post(id)


@blog.route("/comment/<int:id>", methods=["POST"])
@login_required
def add_comment(id):
    """Add comment to post"""
    form = CommentForm()
    return comment_utils.add_comment(id, form, current_user._id)


@blog.route("/comment/delete/<int:id>")
@login_required
def delete_comment(id):
    """Delete comment from post"""
    return comment_utils.delete_comment(id, current_user._id)
